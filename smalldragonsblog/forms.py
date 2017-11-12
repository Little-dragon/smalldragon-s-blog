#coding = utf-8

from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , BooleanField , TextField
from wtforms.validators import DataRequired , Length , EqualTo
from smalldragonsblog.models import User

class LoginForm(FlaskForm):
    username = StringField(
        'Name' , validators=[DataRequired() , Length(max=255)]
    )
    password = PasswordField('Password' , validators=[DataRequired() , Length(min=6)])
    remember = BooleanField('Remember Me')

    # 在调用validate_on_submit的回调函数
    def validate(self):
        check_validate = super(LoginForm , self).validate()

        if not check_validate:
            return False

        # 先检查用户是否存在
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False


        # 后检查用户密码是否正确
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password.')
            return False

        return True

class RegisterForm(FlaskForm):
    username = StringField('Username' , [DataRequired() , Length(max=255)])
    password = PasswordField('Password' , [DataRequired() , Length(min=6)])
    confirm = PasswordField('Confirm Password' , [DataRequired() , EqualTo('password')])

    def validate(self):
        check_validate = super(RegisterForm , self).validate()

        # 首先要通过表单验证
        if not check_validate:
            return False

        # 检查注册用户是否存在
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('用户名已存在！')
            return False
        return True

class CommentForm(FlaskForm):
    name = StringField("Name" , validators=[DataRequired() , Length(max=255)])
    text = TextField("Comment" , validators=[DataRequired()])