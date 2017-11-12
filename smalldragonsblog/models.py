#coding = utf-8

from flask_sqlalchemy import SQLAlchemy
from smalldragonsblog.extensions import bcrypt
from flask_login import AnonymousUserMixin
db = SQLAlchemy()

posts_tags = db.Table('posts_tags',
    db.Column('post_id', db.String(45), db.ForeignKey('posts.id')),
    db.Column('tag_id', db.String(45), db.ForeignKey('tags.id')))

users_roles = db.Table('users_roles' ,
                      db.Column('user_id' , db.String(45) , db.ForeignKey('users.id')),
                      db.Column('role_id' , db.String(45) , db.ForeignKey('roles.id')))

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.String(45) , primary_key=True)
    name = db.Column(db.String(255) , unique=True)
    description = db.Column(db.String(255))

    def __init__(self , id , name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Model Role '{}'>".format(self.name)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(45) , primary_key=True)
    username = db.Column(db.String(255) , unique=True)
    password = db.Column(db.String(255))
    # 一对多设置（Posts）
    posts = db.relationship('Post' ,
                            backref='users',
                            lazy='dynamic')
    # 多对多设置（Roles）
    roles = db.relationship('Role',
                            secondary=users_roles,
                            backref=db.backref('users',lazy='dynamic'))

    def __init__(self , id , username , password):
        self.id = id
        self.username = username
        self.password = self.set_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self , password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self , password):
        return bcrypt.check_password_hash(self.password , password)

    def is_authenticated(self):
        """Check the user whether logged in."""

        # Check the User's instance whether Class AnonymousUserMixin's instance.
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        """Check the user whether pass the activation process."""

        return True

    def is_anonymous(self):
        """Check the user's login status whether is anonymous."""

        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        """Get the user's uuid from database."""

        return self.id


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.String(45) , primary_key=True)
    title = db.Column(db.String(255) , nullable=False)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    # 设置外键
    user_id = db.Column(db.String(45) , db.ForeignKey('users.id'))
    comments = db.relationship('Comment' , backref='posts' , lazy='dynamic')

    tags = db.relationship('Tag' , secondary=posts_tags , backref=db.backref('posts' , lazy='dynamic'))

    def __init__(self , title):
        self.title = title

    def __repr__(self):
        return "<Model Post '{}'>".format(self.title)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String(45) , primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    post_id = db.Column(db.String(45) , db.ForeignKey('posts.id'))

    def __init__(self, id , title):
        self.id = id
        self.title = title

    def __repr__(self):
        return "<Model Comment '{}'".format(self.title)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.String(45) , primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self , id , name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "Model Tag '{}'".format(self.name)
