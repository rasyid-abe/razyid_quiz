from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app_.models.quiz_model import Subject, Question, Score
from app_ import db

subject = Blueprint('subject', __name__)

@subject.route('/')
@login_required
def index():
    data = {}
    data['title'] = 'Subject Quiz'
    subjects = Subject.query.all()
    return render_template('subject/subject.html', user=current_user, subjects=subjects, data=data)

@subject.route('/add', methods=['GET', 'POST'])
@login_required
def subject_add():
    data = {}
    data['title'] = 'Add Subject Quiz'
    data['heading'] = 'Error'
    data['status'] = 'error'

    if request.method == 'POST':    
        subject = request.form.get('subject')
        description = request.form.get('description')

        new_subject = Subject(subject=subject, description=description)
        db.session.add(new_subject)
        db.session.commit()

        data['status'] = 'success'
        data['heading'] = 'Success'
        data['message'] = 'Subject created!'

    return render_template('subject/subject_add.html', user=current_user, data=data)


@subject.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def subject_edit(id):
    data = {}
    data['title'] = 'Edit Subject Quiz'
    data['heading'] = 'Error'
    data['status'] = 'error'

    update_subject = Subject.query.filter_by(id=id).first()
    data['row'] = update_subject

    if request.method == 'POST':
        update_subject.subject = request.form.get('subject')
        update_subject.description = request.form.get('description')
        
        db.session.commit()

        data['status'] = 'success'
        data['heading'] = 'Success'
        data['message'] = 'Subject updated!'

    return render_template('subject/subject_edit.html', user=current_user, data=data)

@subject.route('/activate/<id>', methods=['GET', 'POST'])
@login_required
def subject_activate(id):
    data = {}
    data['heading'] = 'Error'
    data['status'] = 'error'

    update_subject = Subject.query.filter_by(id=id).first()
    data['row'] = update_subject

    if request.method == 'GET':
        sts_msg = 'Success Activate!' if update_subject.is_active == False else 'Success Deactivate!'
        new_sts = True if update_subject.is_active == False else False

        update_subject.is_active = new_sts
        db.session.commit()

        data['status'] = 'success'
        data['heading'] = 'Success'
        data['message'] = sts_msg

    return redirect(url_for('subject.index'))

@subject.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def subject_delete(id):
    
    Subject.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('subject.index'))
