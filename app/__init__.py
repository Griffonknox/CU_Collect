from flask import Flask
from .config import SECRET_KEY
from flask_login import LoginManager


app = Flask(__name__)


login_manager = LoginManager()
login_manager.init_app(app)


app.config['SECRET_KEY'] = SECRET_KEY