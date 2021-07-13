"""Create database models to represent tables."""
from air3d_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """User model, for attorneys only)."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    # # One-to-many relationship: each user can have many requests posts
    requests = db.relationship('Requests', back_populates='author')
    profile = db.relationship('Profile', back_populates='user', uselist=False)
    

    def __repr__(self):
        return f'<User: {self.username}>'

class Profile(db.Model):
    """Owner profile model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    # One-to-one relationship: each user has exactly one profile
    user = db.relationship('User', back_populates='profile', uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creation_date = db.Column(db.Date)

class Requests(db.Model):
    """Requests model."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    submission_date = db.Column(db.Date)
    user = db.relationship('User', back_populates='requests')

class Design(db.Model):
    """Design upload model."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    submission_date = db.Column(db.Date)