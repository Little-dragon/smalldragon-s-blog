#coding = utf-8

from flask_restful import Resource , marshal_with ,fields
from flask import abort
from smalldragonsblog.models import User

post_fields = {
    'username' : fields.String(),
    'password' : fields.String()
}

class PostApi(Resource):
    @marshal_with(post_fields)
    def get(self):
        return {'Hello' : 'world'}