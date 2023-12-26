from app_ import db
from datetime import datetime
from .users_model import User

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(128), index=True, nullable=False)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id))
    question = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(128))
    option_str = db.Column(db.Boolean, default=True)
    arr_option = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    answer_explanation = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id))
    score = db.Column(db.Integer, nullable=False)
    finish_by = db.Column(db.String(16), nullable=False)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id))
    answer = db.Column(db.String(255))
    poin = db.Column(db.Integer, nullable=False)

