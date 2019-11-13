from flask import Flask
from flask_pymongo import PyMongo
from config import config
# 创建数据库
mongo = PyMongo()


def create_app(config_name):
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object(config[config_name])
    # 初始化数据库
    mongo.init_app(app)
    # 导入蓝图，在app目录下面建一个test模块
    from .test import blue as test_blueprint
    # 注册蓝图
    app.register_blueprint(test_blueprint, url_prefix='/api/v1')

    return app
