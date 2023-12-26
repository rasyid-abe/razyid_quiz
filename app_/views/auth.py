from flask import Blueprint, render_template, request, redirect, url_for
from app_ import db
from app_.models.users_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    data = {}
    data['heading'] = 'Error'
    data['status'] = 'error'

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('dashboard.index'))
            else:
                data['message'] = 'Wrong password!'
        else:
            data['message'] = 'Account is not registered!'

    return render_template('auth/signin.html', data=data)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def register():
    data = {}
    data['heading'] = 'Error'
    data['status'] = 'error'
    
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password != confirm:
            data['message'] = 'Password don\'t match!'
        elif len(password) < 8:
            data['message'] = 'Password at least 8 characters!'
        else:
            email_exists = User.query.filter_by(email=email).first()
            if email_exists:
                data['message'] = 'Email has been registered!'
            else:
                new_user = User(email=email, name=fullname, password=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()

                data['status'] = 'success'
                data['heading'] = 'Success'
                data['message'] = 'Account created!'

    return render_template('auth/signup.html', data=data)