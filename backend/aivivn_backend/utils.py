from functools import wraps

from flask_login import current_user
from flask_restful import abort
from webargs.flaskparser import parser
from pony.orm import ObjectNotFound, TransactionIntegrityError, ConstraintError

from .models import Participation


# class CustomEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return str(obj)
#         elif isinstance(obj, datetime.date):
#             return str(obj)
#         return json.JSONEncoder.default(self, obj)


# def custom_json_output(data, code, headers=None):
#     dumped = json.dumps(data, cls=CustomEncoder)
#     resp = make_response(dumped, code)
#     resp.headers.extend(headers or {})
#     return resp


def require_object(entity_cls, src_field=None, get_fn=None, tgt_field=None):
    """
    convert entity_id to Entity object
    :param tgt_field: name of target param (default: entity_cls.__name__.lower())
    :param get_fn: use as query function if specified
    :param entity_cls: entity class
    :param src_field: name of source param, default entity_cls.__name__.lower() + "_id"
    :return: decorator
    """

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            _src_field = src_field or (entity_cls.__name__.lower() + "_id")
            if _src_field in kwargs:
                try:
                    obj = entity_cls[kwargs[_src_field]] if get_fn is None \
                        else get_fn(**kwargs)
                except ObjectNotFound:
                    abort(404, error='error_resource_not_found')
                del kwargs[_src_field]
                kwargs[tgt_field or entity_cls.__name__.lower()] = obj
            else:
                raise ValueError('Entity field does not exist.')
            return f(*args, **kwargs)

        return decorated

    return decorator


def require_my_team(is_leader=False):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            contest = kwargs['contest']
            p = Participation.get_team_by_user(contest, current_user.id, is_leader)
            if not p:
                if is_leader:
                    abort(403, error='error_unauthorized')
                else:
                    abort(404, error='error_resource_not_found')
            return f(*args, my_team=p, **kwargs)
        return decorated
    return decorator


def clean_pony_error(e):
    return str(e).strip().split('\n')[-1].split(':')[-1].strip()


def handle_db_errors(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except TransactionIntegrityError as e:
            abort(422, message=clean_pony_error(e), error='error_transaction_integrity')
        except ConstraintError as e:
            abort(422, message=clean_pony_error(e), error="error_constraint")
        except Exception as e:
            print(e)
            raise e
    return decorated


def require_login(f):
    @wraps(f)
    def decorared(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401, error='error_unauthorized')
        return f(*args, **kwargs)
    return decorared


@parser.error_handler
def handle_args_error(error, req, schema):
    abort(400, message=error.messages, error="error_params")
