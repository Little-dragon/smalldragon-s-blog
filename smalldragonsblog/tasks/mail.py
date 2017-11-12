#coding = utf-8
from flask_mail import Message
from smalldragonsblog.extensions import flask_celery , mail
from smalldragonsblog.models import Post

@flask_celery.task
def add_together(num1 , num2):
    return num1 + num2

@flask_celery.task
def remind():
    post = Post.query.filter_by(text='EXAMPLE TEXT').first()
    msg = Message("Your reminder" ,
          sender="2596063092@qq.com" ,
          recipients=['2596063092@qq.com'])
    msg.body = post.text
    mail.send(msg)