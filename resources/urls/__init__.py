# 蓝图
from flask import Blueprint
from flask_restful import Api

from utli.output import output_json
from .login import LoginView, CodeView, UserView

# Channel,  Profile

user_api = Blueprint('user_api', __name__)  # 创建蓝图
news_app = Api(user_api, catch_all_404s=True)  # 创建蓝图的路由
news_app.representation('application/json')(output_json)  # 设置输出格式

news_app.add_resource(LoginView, '/app/v1_0/authorizations')  # 添加路由
news_app.add_resource(CodeView, '/app/v1_0/sms/codes/<string:mobile>')  # 添加路由
# news_app.add_resource(Channel, '/app/v1_0/channels')
news_app.add_resource(UserView, '/app/v1_0/user')
# news_app.add_resource(Profile, '/app/v1_0/user/profile')
