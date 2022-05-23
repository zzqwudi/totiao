# 蓝图
from flask import Blueprint
from flask_restful import Api
from .login import LoginView, CodeView, Channel, UserView, Profile

user_api = Blueprint('user_api', __name__)  # 创建蓝图
user_app = Api(user_api)  # 创建蓝图的路由

user_app.add_resource(LoginView, '/app/v1_0/authorizations')
user_app.add_resource(CodeView, '/app/v1_0/sms/codes/<string:mobile>')
user_app.add_resource(Channel, '/app/v1_0/channels')
user_app.add_resource(UserView, '/app/v1_0/user')
user_app.add_resource(Profile, '/app/v1_0/user/profile')
