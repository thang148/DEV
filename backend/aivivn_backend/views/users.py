from flask import Blueprint
from flask_login import current_user
from flask_restful import abort, Resource, Api, marshal_with
from pony.orm import commit, select, desc
from webargs.flaskparser import use_kwargs, use_args

from ..fields_req import login_args, pagination_args, user_me_args, signup_args
from ..fields_res import user_basic_fields, user_fields, user_me_fields
from ..models import User
from ..utils import handle_db_errors, require_login


class UserListResource(Resource):
    @use_kwargs(pagination_args)
    @marshal_with(user_basic_fields)
    def get(self, limit, offset):
        users = list(select(u for u in User).order_by(desc(User.ranking_point))[offset:offset + limit])
        return users

    @use_args(signup_args)
    def post(self, args):
        user = User(**args)
        commit()
        return dict(user_id=user.id)


class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, uid):
        return User[uid] if uid.isdigit() else User.get(username=uid)


class MeResource(Resource):
    @marshal_with(user_me_fields)
    @require_login
    def get(self):
        return User[current_user.id]

    @use_args(user_me_args)
    @marshal_with(user_me_fields)
    @require_login
    def patch(self, args):
        user = User[current_user.id]
        user.set(**args)
        return user


class LoginResource(Resource):
    @use_kwargs(login_args)
    def post(self, username, password):
        user = select(
            u for u in User
            if u.username == username or u.email == username
        ).first()
        if not (user and user.check_password(password)):
            abort(422, error='error_wrong_username_or_password')
        return dict(access_token=user.generate_token())


bp = Blueprint('users', __name__)
api = Api(bp, decorators=[handle_db_errors])
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<uid>')
api.add_resource(LoginResource, '/users/login')
api.add_resource(MeResource, '/me')
