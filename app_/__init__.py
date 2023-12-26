from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'flaskquiz123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views.dashboard import dashboard
    from .views.auth import auth
    from .views.subject import subject
    from .views.question import question
    from .views.user import user
    from .views.quiz import quiz

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(quiz, url_prefix='/quiz')
    app.register_blueprint(dashboard, url_prefix='/home')
    app.register_blueprint(subject, url_prefix='/subject')
    app.register_blueprint(question, url_prefix='/question')

    from .models.users_model import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = '/'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

        