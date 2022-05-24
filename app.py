from flask import Flask

from config import Config
from resources.news import news_bp
from resources.urls import user_api
from utli.middlewares import jwt_authentication
from utli.snowflake.id_worker import IdWorker

app = Flask(__name__)  # 创建Flask实例
app.config.from_object(Config)  # 导入配置文件
app.register_blueprint(user_api)  # 注册蓝图
app.register_blueprint(news_bp)

app.before_request(jwt_authentication)
app.id_worker = IdWorker(app.config['DATACENTER_ID'],
                         app.config['WORKER_ID'],
                         app.config['SEQUENCE'])  # 初始化id生成器
from models import db  # 初始化数据库

db.init_app(app)  # 初始化数据库


@app.route('/')  # 路由
def index():  # 视图函数
    return 'ok'  # 返回值


if __name__ == '__main__':
    app.run()
