#coding = utf-8

#解决循环导入
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Api
from datetime import timedelta
from flask_principal import Principal , Permission , RoleNeed
from flask_celery import Celery
from flask_cache import Cache
from flask_mail import Mail
from flask_assets import Environment , Bundle
from flask_admin.contrib.sqla import ModelView

assets_env = Environment()
main_css = Bundle('css/base.css',
                  filters='cssmin',
                  output='assets/css/common.css')

# my_admin = Admin()
bcrypt = Bcrypt()
login_manager = LoginManager()
rest_api = Api()
flask_celery = Celery()
mail = Mail()
cache = Cache()

# Setup the configuration for login manager.
#     1. Set the login page.
#     2. Set the more stronger auth-protection.
#     3. Show the information when you are logging.
#     4. Set the Login Messages type as `information`.
# 下面设置内容会出现在重定向的页面上
login_manager.login_view = "form"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"
# 设置cookie过期时间为一天，默认为一年
login_manager.remember_cookie_duration = timedelta(days=1)

principals = Principal()
# 设置三种权限
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

@login_manager.user_loader
def load_user(user_id):
    """Load the user's info"""

    from smalldragonsblog.models import User
    return User.query.filter_by(id=user_id).first()