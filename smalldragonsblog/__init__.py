import pymysql
from flask import Flask, render_template, \
    request, redirect, url_for, flash , abort , make_response , g , session , Blueprint
from flask_login import login_required, login_user , current_user ,logout_user
from smalldragonsblog.controllers import blog
from flask_admin import Admin
from smalldragonsblog.controllers.admin import CustomView , CustomModelView , MyView
from smalldragonsblog.config import DevConfig , Config
from smalldragonsblog.extensions import bcrypt, login_manager , rest_api , flask_celery , admin_permission ,\
    cache , assets_env , main_css , mail
from flask_principal import UserNeed , identity_loaded , identity_changed , RoleNeed
from smalldragonsblog.forms import LoginForm , RegisterForm , CommentForm
from smalldragonsblog.models import User, db , Comment , Post , Tag , posts_tags , Role


# 利用工厂模式创建应用对象
def create_app(object_name):

    pymysql.install_as_MySQLdb()
    app = Flask(__name__)
    app.config.from_object(object_name)

    flask_celery.init_app(app)
    # celery.conf.update(app.config)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    rest_api.init_app(app)
    cache.init_app(app)
    assets_env.init_app(app)
    assets_env.register("main_css" , main_css)
    # 从extension中导入的话会造成重复蓝图错误,所以直接在这里初始化
    admin = Admin(app)
    admin.add_view(CustomView(name="Hello"))
    models = [Role , Tag]
    for model in models:
        admin.add_view(CustomModelView(model , db.session , category="Models"))
    admin.add_view(MyView(db.session))
    mail.init_app(app)

    # 身份初始化，添加角色到身份中
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
    app.register_blueprint(blog.blog_blueprint)
    return app

app = create_app(DevConfig)
if __name__ == '__main__':
    print(app.view_functions)
    print(app.url_map)
    app.run()