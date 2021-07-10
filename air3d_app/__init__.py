import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from air3d_app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# from air3d_app.main.routes import main
# from air3d_app.auth.routes import auth
# from air3d_app.auth.tests import tests
# app.register_blueprint(main)
# app.register_blueprint(auth)
# app.register_blueprint(tests)

from air3d_app.main.routes import main as main_routes
app.register_blueprint(main_routes)

from air3d_app.auth.routes import auth as auth_routes
app.register_blueprint(auth_routes)

with app.app_context():
    db.create_all()
