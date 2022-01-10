import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from air3d_app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

# Initialize SocketIO for chat
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Limits file upload size to 16mb
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# Sets config properties for flask uploads
OFFERS_FOLDER = './uploads/offers'
app.config["UPLOADED_OFFERS_DEST"] = OFFERS_FOLDER
REQUESTS_FOLDER = './uploads/requests'
app.config["UPLOADED_REQUESTS_DEST"] = REQUESTS_FOLDER

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Login setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


from .models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from air3d_app.main.routes import main as main_routes
app.register_blueprint(main_routes)

from air3d_app.auth.routes import auth as auth_routes
app.register_blueprint(auth_routes)

with app.app_context():
    db.create_all()
