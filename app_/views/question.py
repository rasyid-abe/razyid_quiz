from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app_.models.quiz_model import Subject, Question, Score
from app_ import db
import json

question = Blueprint('question', __name__)

def extract_row(datas):
    result_quest = []
    for i in datas:
        quest = {}
        quest['question'] = ''.join(i.question)
        quest['option_1'] = json.loads(i.arr_option)[0]
        quest['option_2'] = json.loads(i.arr_option)[1]
        quest['option_3'] = json.loads(i.arr_option)[2]
        quest['option_4'] = json.loads(i.arr_option)[3]
        quest['answer'] = i.answer
        quest['answer_explanation'] = i.answer_explanation
        quest['id'] = i.id
        quest['subject_id'] = i.subject_id
        result_quest.append(quest)
    return result_quest

@question.route('/<id>')
@login_required
def show(id):
    data = {}

    subject = Subject.query.filter_by(id=id).first()
    data['title'] = f'Question {subject.subject}'
    data['subject_id'] = id
    
    questions = Question.query.filter_by(subject_id=id)
    result_quest = extract_row(questions)

    return render_template('question/question.html', user=current_user, questions=result_quest, data=data)

@question.route('/add/<subject>', methods=['GET', 'POST'])
@login_required
def question_add(subject):
    data = {}
    data['title'] = 'Add Question'
    data['heading'] = 'Error'
    data['status'] = 'error'
    data['subject_id'] = subject
    data['question'] = Question.query.filter_by(subject_id=subject)

    if request.method == 'POST':    
        subject_id = request.form.get('subject_id')
        question = request.form.get('question')
        arr_option = json.dumps([request.form.get('option_1'),request.form.get('option_2'),request.form.get('option_3'),request.form.get('option_4')])
        answer = request.form.get('answer')
        answer_explanation = request.form.get('answer_explanation')

        new_question = Question(subject_id=subject_id, question=question, arr_option=arr_option, answer=answer, answer_explanation=answer_explanation)
        db.session.add(new_question)
        db.session.commit()

        data['status'] = 'success'
        data['heading'] = 'Success'
        data['message'] = 'Question created!'

    return render_template('question/question_add.html', user=current_user, data=data)


@question.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def question_edit(id):
    data = {}
    data['title'] = 'Edit Question'
    data['heading'] = 'Error'
    data['status'] = 'error'

    update_question = Question.query.filter_by(id=id).first()
    data['row'] = update_question
    data['row_option'] = json.loads(update_question.arr_option)

    if request.method == 'POST':
        update_question.question = request.form.get('question')
        update_question.arr_option = json.dumps([request.form.get('option_1'),request.form.get('option_2'),request.form.get('option_3'),request.form.get('option_4')])
        update_question.answer = request.form.get('answer')
        update_question.answer_explanation = request.form.get('answer_explanation')

        db.session.commit()

        update_question = Question.query.filter_by(id=id).first()
        data['row'] = update_question
        data['row_option'] = json.loads(update_question.arr_option)

        data['status'] = 'success'
        data['heading'] = 'Success'
        data['message'] = 'Question updated!'

    return render_template('question/question_edit.html', user=current_user, data=data)

@question.route('/delete/<subject>/<id>', methods=['GET', 'POST'])
@login_required
def question_delete(subject, id):
    
    Question.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('question.show', id=subject))
