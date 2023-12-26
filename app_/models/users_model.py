from app_ import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.SmallInteger, default=1, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    user_role = db.Column(db.SmallInteger, default=2, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)