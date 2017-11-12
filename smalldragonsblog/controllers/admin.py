#coding = utf-8
from flask_admin import BaseView , expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import widgets , TextAreaField
from smalldragonsblog.models import User , Post

class CustomView(BaseView):

    # def is_accessible(self):
    #     return current_user.is_authenticated

    @expose('/')
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    def second_page(self):
        return self.render('admin/second_page.html')

class CustomModelView(ModelView):
    pass


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_' , 'ckeditor')
        return super(CKTextAreaWidget , self).__call__(field , **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class MyView(ModelView):
    form_overrides = dict(text=CKTextAreaField)
    column_searchable_list = ('text' , 'title')
    # column_filters = ('publish_date')
    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'
    # Disable model creation
    # can_create = False

    # Override displayed fields
    # column_list = ('username', 'email')
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyView, self).__init__(Post , session, **kwargs)