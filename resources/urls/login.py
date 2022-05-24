from datetime import datetime, timedelta

from flask import request, current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from redis import Redis

from models import db
from models.user import User, UserProfile
from utli import parser
from utli.jwt_util import generate_jwt
from utli.middlewares import g


class LoginView(Resource):
    def _generate_token(self, user_id, refresh=True):
        payload = {
            'user_id': user_id,
            'refresh': refresh
        }
        print(payload)
        expires = datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRY_HOURS'])
        token = generate_jwt(payload, expires)

        if refresh:
            expiry = datetime.utcnow() + timedelta(hours=current_app.config['JWT_REFRESH_DAYS'])
            refresh_token = generate_jwt(payload, expiry)
        else:
            refresh_token = None
        return token, refresh_token

    def post(self):
        json_parser = RequestParser()
        json_parser.add_argument('mobile', required=True, location='json', type=parser.mobile)
        json_parser.add_argument('code', required=True, location='json', type=parser.code)
        args = json_parser.parse_args()
        mobile = args.get('mobile')
        code = args.get('code')
        mobile_code = f'mobile_{mobile}'
        redis_cli = Redis(host='127.0.0.1', port=6379, db=0)
        mobile_code_value = redis_cli.get(mobile_code)
        if not mobile_code_value:
            return {'message': 'code is invalid'}, 400
        if code != mobile_code_value.decode('utf-8') if mobile_code_value else 0:
            return {'message': 'code is invalid'}, 400
        user = User.query.filter_by(mobile=mobile).first()
        if not user:
            user_id = current_app.id_worker.get_id()
            user = User(id=user_id, mobile=mobile, name=mobile, last_login=datetime.now())
            db.session.add(user)
            profile = UserProfile(id=user.id)
            db.session.add(profile)
            db.session.commit()
        else:
            if user.status == User.STATUS.DISABLE:
                return {'message': 'Invalid user.'}, 403
        token, refresh_token = self._generate_token(user.id)  # 生成token
        return {'token': token, 'refresh_token': refresh_token}, 201


class CodeView(Resource):
    def get(self, mobile):
        code = self.my_code()
        exc_time = 42 * 60
        try:
            parser.mobile(mobile_code=mobile)
        except ValueError:
            return {'message': 'mobile is invalid'}, 404
        mobile_code = f'mobile_{mobile}'
        first_code = f'first_{mobile}'
        redis_cli = Redis(host='127.0.0.1', port=6379, db=0)
        first_code_value = redis_cli.get(first_code)
        if first_code_value:
            return {'message': 'SMS has been sent, no need to send again'}, 429
        pl = redis_cli.pipeline()
        pl.setex(mobile_code, value=code, time=exc_time)
        pl.setex(first_code, value=1, time=exc_time)
        pl.execute()
        print(code)
        # ret = send_message.delay(mobile, code, exc_time)
        # if ret:
        return {'message': 'ok', 'mobile': mobile}, 200
        # return {'message': 'not ok', 'mobile': mobile}, 429

    @staticmethod
    def my_code():
        import random
        import string
        return ''.join(random.choices(string.digits, k=6))


class Channel(Resource):
    def get(self):
        pass


class UserView(Resource):  # 用户信息
    def get(self):
        token = request.headers.get('Authorization')  # 获取token
        id = g.user_id
        user = User.query.filter_by(id=id).first()  # 查询user
        if not user:
            return {'message': 'Invalid user.'}, 403
        dict = {
            'id': user.id,
            'mobile': user.mobile,
            'name': user.name,
            'photo': user.profile_photo,
            'art_count': user.article_count,
            'follow_count': user.following_count,
            'fans_count': user.fans_count,
            'like_count': user.like_count,
        }
        return {'message': 'ok', 'data': dict}, 200


class Profile(Resource):
    def get(self):
        pass
        # # 获取登录
        # print(1111)
        # token = request.headers.get('Authorization') # 获取token
        # if not token:
        #     return jsonify({'code': 0, 'message': 'Please login first'})
        # payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        # user_id = payload.get('user_id')
        # user = User.query.get(user_id)
        # print(user_id, 3333)
        # return {'mobile': '13800138000'}, 200
