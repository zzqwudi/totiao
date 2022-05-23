from flask import Flask
from config import Config
from utli.middlewares import jwt_authentication
from resources.urls import user_api

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(user_api)  # 注册蓝图
app.before_request(jwt_authentication)
if __name__ == '__main__':
    app.run()
