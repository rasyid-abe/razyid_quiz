from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app_.models.users_model import User
from app_ import db

user = Blueprint('user', __name__)

@user.route('/')
@login_required
def index():
    data = {}
    data['title'] = 'User'
    users = User.query.all()
    return render_template('user/user.html', user=current_user, users=users, data=data)
