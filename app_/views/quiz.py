from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql import func, desc
from app_.models.quiz_model import Subject, Score, Question, Answer
from app_.models.users_model import User
from app_ import db
import json
import random

quiz = Blueprint('quiz', __name__)

@quiz.route('/')
@login_required
def index():
    data = {}
    data['title'] = 'Quiz'

    subjects = Subject.query.filter_by(is_active=True)
    r_sub = []
    for i in subjects:
        c_score = Score.query.filter_by(subject_id=i.id, user_id=current_user.id).first()
        
        c_sub = {}
        c_sub['id'] = i.id
        c_sub['subject'] = i.subject
        c_sub['description'] = i.description
        c_sub['is_taken'] = 0 if c_score == None else c_score.id
        
        r_sub.append(c_sub)

    data['subjects'] = r_sub
    
    return render_template('quiz/quiz.html', user=current_user, data=data)

@quiz.route('/result/<id>', methods=['GET', 'POST'])
@login_required
def result(id):
    data = {}

    subject = Subject.query.filter_by(id=id).first()
    question = Question.query.filter_by(subject_id=id).order_by(Question.id)
    answer = Answer.query.filter_by(user_id=current_user.id, subject_id=id).order_by(Answer.question_id)
    question = extract_row(question)
    
    data['question'] = question
    data['answer'] = answer
    data['title'] = f'Quiz {subject.subject}'
    data['subject_id'] = id

    return render_template('quiz/result.html', user=current_user, data=data)

@quiz.route('/result_quiz/<id>', methods=['GET'])
@login_required
def result_quiz(id):
    data = {}

    score = Score.query\
        .join(User, Score.user_id == User.id)\
        .join(Subject, Score.subject_id == Subject.id)\
        .filter(Subject.id == id)\
        .filter(User.id == current_user.id)\
        .add_columns(Score.id, User.name, Subject.subject, Score.score).first()

    data['score'] = score
    data['title'] = 'Result Quiz'
    data['subject_id'] = id

    return render_template('quiz/result_quiz.html', user=current_user, data=data)

@quiz.route('/leaderboard', methods=['GET'])
@login_required
def leaderboard():
    data = {}

    score = Score.query\
        .join(User, Score.user_id == User.id)\
        .join(Subject, Score.subject_id == Subject.id)\
        .filter(User.user_role == 2)\
        .add_columns(Score.id, User.name, Subject.subject, Score.score)

    data['score'] = score
    data['title'] = 'Leaderboard'
    data['subject_id'] = id

    return render_template('quiz/leaderboard.html', user=current_user, data=data)

@quiz.route('/take/<id>', methods=['GET', 'POST'])
@login_required
def take(id):
    data = {}

    subject = Subject.query.filter_by(id=id).first()
    question = Question.query.filter_by(subject_id=id).order_by(func.random())
    question = extract_row(question)
    
    data['question'] = question
    data['title'] = f'Quiz {subject.subject}'
    data['subject_id'] = id

    if request.method == 'POST':
        # answer = {}
        t_poin = 0
        for i in question:
            poin = 10 if i['answer'] == request.form.get(f'{i['id']}') else 0
            new_answer = Answer(
                user_id = current_user.id,
                question_id = i['id'],
                subject_id = id,
                answer = request.form.get(f'{i['id']}'),
                poin = poin
            )
            db.session.add(new_answer)
            db.session.commit()

            # answer[i['id']] = request.form.get(f'{i['id']}')
            t_poin = t_poin + poin

        new_score = Score(
            user_id = current_user.id,
            subject_id = id,
            score = t_poin,
            finish_by = request.form.get('submit')
        )

        db.session.add(new_score)
        db.session.commit()

        return redirect(url_for('quiz.result_quiz', id=id))
    
    return render_template('question.html', user=current_user, data=data)


def extract_row(datas):
    result_quest = []
    for i in datas:
        quest = {}
        quest['question'] = ''.join(i.question)
        quest['arr_option'] = random.sample(json.loads(i.arr_option), len(json.loads(i.arr_option)))
        quest['answer'] = i.answer
        quest['answer_explanation'] = i.answer_explanation
        quest['id'] = i.id
        quest['subject_id'] = i.subject_id
        result_quest.append(quest)

    return result_quest
