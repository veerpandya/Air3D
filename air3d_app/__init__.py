from dotenv import load_dotenv
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
app.secret_key = os.getenv('SECRET_KEY')

mongo = PyMongo(app)
bcrypt = Bcrypt(app)


from air3d_app.main.routes import main
from air3d_app.auth.routes import auth
app.register_blueprint(main)
app.register_blueprint(auth)
