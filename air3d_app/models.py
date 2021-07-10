"""Create database models to represent tables."""
from air3d_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """User model, for attorneys only)."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    # # One-to-many relationship: each user can have many forum posts
    # forum_posts = db.relationship('Forum', back_populates='author')
    # # One-to-one relationship: each user has exactly one profile
    # profile = db.relationship('Profile', back_populates='user', uselist=False)
    # profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'