import os

from flask import Flask
from flask_login import LoginManager
from pony.flask import Pony

from .cache import cache
from .models import db, User
from .views import users as users_view, contests as contests_view

app = Flask(__name__)

config_class = (os.getenv('FLASK_ENV') or 'test').title() + 'Config'
app.config.from_object(f'aivivn_backend.config.{config_class}')

db.bind(**(app.config['PONY_PROVIDER']))
db.generate_mapping(create_tables=app.config['ENV'] != 'production')

Pony(app)

login_manager = LoginManager(app)

cache.init_app(app, config=app.config)


@login_manager.header_loader
def load_user_from_header(header_val):
    access_token = header_val.replace('Bearer ', '', 1)
    return User.get_user_from_token(access_token)


@app.route('/ping')
def ping():
    return 'pong'


app.register_blueprint(users_view.bp)
app.register_blueprint(contests_view.bp)
