from flask import request, current_app, g, abort

from utli.jwt_util import verify_jwt


def jwt_authentication():  # 认证中间件
    if not request.path.startswith('/app/v1_0/sms/codes/') and \
            not request.path.startswith('/app/v1_0/authorizations') :  # 如果不是登录接口
        token = request.headers.get('Authorization', '')  # 获取token
        if not token:  # 如果token不存在
            abort(403)  # 抛出403错误
        token = token.split('Bearer ')[1]
        payload = verify_jwt(token=token, secret=current_app.config['JWT_SECRET'])  # 验证token
        if not payload:  # 如果验证失败
            abort(403)  # 抛出403错误
        g.user_id = payload.get('user_id')  # 获取用户id
