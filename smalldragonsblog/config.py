#coding = utf-8
import os
from datetime import timedelta

class Config(object):
    SECRET_KEY = os.urandom(24)
    # RECAPTCHA_PUBLIC_KEY = '6LeBmjQUAAAAAJWWOPfp3i0rqB4dQwxmDXcO4llc'
    # RECAPTCHA_PRIVATE_KEY = '6LeBmjQUAAAAAKvYO_OPmqkBU2CT2mtcwXr7kS6y'

    #设置session过期时间为5分钟
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CACHE_TYPE = 'simple'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    # 开发者环境不使用assets(需要不停修改资源)
    ASSETS_DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '2596063092@qq.com'
    # 此密码不是qq密码,qq邮箱生成的授权码
    MAIL_PASSWORD = 'qcrxwfiftnendjdi'
    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = 'root'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'test1'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
