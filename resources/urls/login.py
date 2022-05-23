from datetime import datetime, timedelta

import jwt
from flask import request, jsonify, current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from redis import Redis

from celery_tasks.sms.tasks import send_message
from models import User
from utli import parser
from utli.database import db_session
from utli.jwt_util import generate_jwt


class LoginView(Resource):
    def _generate_token(self, user_id, refresh=False):
        payload = {
            'user_id': user_id,
            'refresh': refresh
        }
        expires = datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRY_HOURS'])
        token = generate_jwt(payload, expires)

        if refresh:
            expiry = datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRY_DAYS'])
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
            return jsonify({'code': 0, 'message': '验证码已过期'})
        if code != mobile_code_value.decode('utf-8') if mobile_code_value else 0:
            return jsonify({'code': 0, 'message': '验证码错误'})
        user = User.query.filter_by(mobile=mobile).first()
        if not user:
            user = User(mobile=mobile)
            db_session.add(user)
            db_session.commit()
            return jsonify({'code': 1, 'msg': '注册成功'})
        else:
            if user.status == User.STATUS.ENABLE:
                return jsonify({'code': 403, 'message': 'Invalid User'})
        token, refresh_token = self._generate_token(user.id)  # 生成token
        return jsonify({'code': 1, 'refresh_token': refresh_token, 'token': token})


class CodeView(Resource):
    def get(self, mobile):
        code = self.my_code()
        print(mobile)
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
        ret = send_message.delay(mobile, code, exc_time)
        if ret:
            return {'message': 'Send SMS successfully'}, 200
        return {'message': 'failed to send SMS'}, 429

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
        print(token,11223)
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])  # 解析token
        print(payload)
        user_id = payload.get('user_id')  # 获取user_id
        user = User.query.filter_by(id=user_id).first()  # 查询user
        print({
            'id': user.id,
            'mobile': user.mobile,
            'status': user.status,
            'create_time': user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        })
        # if not user:
        #     return {'code': 0, 'message': 'user is invalid'}, 404
        # return {'message': 'success', 'data': {'user': user.to_json()}}, 200  # 返回用户信息


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
