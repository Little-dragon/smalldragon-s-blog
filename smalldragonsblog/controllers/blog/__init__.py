from os import path
from flask import Flask, render_template, \
    request, redirect, url_for, flash , abort , make_response , g , session , Blueprint
from flask_login import login_required, login_user , current_user ,logout_user
from uuid import uuid4
from smalldragonsblog.extensions import cache
import datetime
from sqlalchemy import func
from smalldragonsblog.forms import LoginForm , RegisterForm , CommentForm
from smalldragonsblog.models import User, db , Comment , Post , Tag , posts_tags
from smalldragonsblog.tasks.mail import remind

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder=path.join(path.pardir , path.pardir , 'templates'),
    url_prefix='/blog')

@cache.cached(timeout=7200,key_prefix='sidebar_data')
def sidebar_data():
    recent = db.session.query(Post).order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(Tag , func.count(posts_tags.c.post_id).label('total')).join(posts_tags).group_by(Tag)\
        .order_by('total DESC').limit(5).all()
    return recent , top_tags

@blog_blueprint.route('/')
# @cache.cached(timeout=60)
def base():
    return render_template('base.html')

@blog_blueprint.route('/mail')
def mail():
    # 这是一个耗时操作
    remind.apply_async()
    return '异步加载完成!!!'

@blog_blueprint.route('/post/<string:post_id>' , methods=['GET' , 'POST'])
# @login_required
# @cache.cached(timeout=60)
def index(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(id=str(uuid4()) , name=form.name.data)
        new_comment.text = form.text.data
        new_comment.publish_date = datetime.datetime.now()
        new_comment.post_id = post_id
        db.session.add(new_comment)
        db.session.commit()

    post = Post.query.get_or_404(post_id)
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    return render_template('post.html' , post=post , recent=recent , form=form)

@blog_blueprint.route('/regist',methods=['GET' , 'POST'])
@cache.cached(timeout=60)
def regist():
    if request.method == 'GET':
        form = RegisterForm()
        return render_template('regist.html' , form=form)
    else:
        form = RegisterForm()
        username = form.username.data
        password = form.password.data
        user = User(id=str(uuid4()),username=username,password=password)
        db.session.add(user)
        db.session.commit()
        flash('您可以登陆了！',category='Success!')
        return redirect(url_for('login'))

@blog_blueprint.route('/sign_in' , methods=['GET' , 'POST'])
@cache.cached(timeout=60)
def login():
    form = LoginForm()

    # 如果已经登陆过，则直接跳转至主页
    if session.get('user_id' , None) is not None:
        return redirect(url_for('index'))

    # 否则进行登陆表单验证，get请求下，参数form.validate_on_submit()为false
    if form.validate_on_submit():
        username = form.username.data
        remember_me = form.remember.data
        user = User.query.filter_by(username=username).first()
        login_user(user , remember=remember_me)
        # 设置session关闭浏览器后不失效
        session.parmanent = True
        flash("You have been logged in.", category="Success!")
        return redirect(url_for('index'))
    return render_template('sign_in.html' , form=form)

    # @app.errorhandler(404)
    # def page_not_found(error):
    #     return render_template('')

@blog_blueprint.route('/<int:page>')
@cache.cached(timeout=60)
def home(page=1):
    posts = Post.query.order_by(
            Post.publish_date.desc()
        ).paginate(page, 10)
    recent , top_tags = sidebar_data()
    return render_template('home.html' , posts = posts , recent=recent , top_tags=top_tags)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self , message , status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

@blog_blueprint.errorhandler(InvalidUsage)
def invalid_usage(error):
    response = make_response(error.message)
    response.status_code = error.status_code
    return response


@blog_blueprint.route('/exception')
@cache.cached(timeout=60)
def exception():
    raise InvalidUsage('No privilege to access the resource', status_code=403)

@blog_blueprint.before_request
def before_request():
    g.user = current_user