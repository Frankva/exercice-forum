from .models import questions as questions_model
from .models.tags import format_tags
from .models import tags as tags_model
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
app.config.from_object('config')
import sys
from .models import answers as answers_model
from .models import votes as votes_model
from .models import people as people_model
from .models import groups as groups_model
from .models import messages as messages_model

from flask import session
from functools import wraps

app.secret_key = app.config['SECRET_KEY']

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return render_template('index.html')

@app.get('/questions/')
@app.get('/questions/<tab>')
def questions_get(tab='Newest'):
    if tab == 'Newest':
        questions = questions_model.select()
    elif tab == 'Votes':
        questions = questions_model.select_order_by_vote()
    return render_template('questions.html', questions=questions)

@app.get('/question/<id>')
def question_get(id):
    person_id = session['person_id'] if 'person_id' in session else None
    question, tags, vote, uservote = questions_model.select_one(id, person_id)
    # question['id'] = id
    answers = answers_model.select(id, person_id)
    return render_template('question.html', question=question, answers=answers,
                           tags=tags, vote=vote, uservote=uservote)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        person_id = session['person_id'] if 'person_id' in session else None
        if person_id is None:
            return {'message':'Error not connected'}, 401
        return f(*args, **kwargs)
    return wrapper

def block_autovoting(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        message_id = request.json['messageId'] 
        person_id = session['person_id']
        if votes_model.get_is_autovoting_commit(message_id, person_id):
            return {'message':'Error you cannot vote for yourself'}, 400
        return f(*args, **kwargs)
    return wrapper

@app.post('/question/<int:id>')
@login_required
def question_post(id):
    answers_model.insert(text=request.form['answer'],
                         person_id=session['person_id'],
                         question_id=id)
    
    return question_get(id)

@app.route('/questions/tagged/<tag>')
@app.route('/questions/tagged/<tag>/<tab>')
def tagged_questions(tag, tab=None):
    if tab is None:
        return redirect(url_for('tagged_questions', tag=tag, tab='Newest'))
    if tab == 'Newest':
        questions = questions_model.select_where_tag(tag)
    elif tab == 'Votes':
        questions = questions_model.select_where_tag_order_by_vote(tag)
    return render_template('questions.html', questions=questions)

    

@app.get('/ask')
def ask_get():
    person_id = session['person_id'] if 'person_id' in session else None
    if person_id is None:
        return redirect(url_for('login_get'))
    return render_template('ask.html')

@app.post('/ask')
@login_required
def ask_post():
    questions_model.insert(title=request.form['title'],
                     body=request.form['body'],
                     tags=format_tags(request.form['tags']),
                     user_id=session['person_id'])
    return ask_get()

@app.route('/tags')
def tags():
    tags = tags_model.select_all()
    return render_template('tags.html', tags=tags)

@app.post('/upvote')
@login_required
@block_autovoting
def upvote():
    message_id = request.json['messageId'] 
    votes_model.insert_vote(is_upvote=True,
                            person_id=session['person_id'],
                            message_id=message_id)
    return {"message":"Ok"}
    

@app.post('/downvote')
@login_required
@block_autovoting
def downvote():
    message_id = request.json['messageId'] 
    votes_model.insert_vote(is_upvote=False, person_id=session['person_id'],
                            message_id=message_id)
    return {"message":"Ok"}

@app.post('/nullify-vote')
@login_required
def nullify_vote():
    message_id = request.json['messageId'] 
    votes_model.delete_vote(person_id=session['person_id'],
                            message_id=message_id)
    return {"message":"Ok"}

@app.post('/login')
def login_post():
    person_id = people_model.get_person_id(request.form['email'],
                                           request.form['password'])
    if person_id is None:
        return redirect(url_for('login_get'))
    session['person_id'] = person_id
    session['email'] = request.form['email']
    return redirect(url_for('index'))

@app.get('/login')
def login_get():
    if 'person_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('person_id', None)
    return redirect(url_for('index'))


@app.get('/signin')
def signin_get():
    if 'person_id' in session:
        return redirect(url_for('index'))
    return render_template('signin.html')

@app.post('/signin')
def signin_post():
    people_model.insert_person(**request.form)
    return redirect(url_for('login_get'))

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not groups_model.is_admin(session['person_id']):
            return {'message':'Error not authorised'}, 401
        return f(*args, **kwargs)
    return wrapper

@app.get('/admin')
@login_required
@admin_required
def admin():
    users = people_model.select_people()
    def f(user):
        user['actions'] = ({'label': 'Voir les messages',
               'url': url_for('admin_person_message',
               person_id=user['person_id'])},
               {'label': 'Voir titres des questions',
               'url': url_for('admin_person_title',
                              person_id=user['person_id'])})
        return user
    users_with_actions = tuple(map(f, users))
    return render_template('admin.html', data_list=users, title='personnes')

@app.get('/admin/<person_id>')
@login_required
@admin_required
def admin_person_message(person_id: int):
    messages = messages_model.select_person_messages(person_id)
    def f(message):
        message['actions'] = ({'label': 'Nullifier',
                'url': url_for('admin_person_message_nullify',
                person_id=person_id, message_id=message['message_id'])}, )
        return message
    messages_with_actions = tuple(map(f, messages))
    return render_template('admin.html', data_list=messages_with_actions,
                           title='messages')

@app.get('/admin/<person_id>/<message_id>')
@login_required
@admin_required
def admin_person_message_nullify(person_id: int, message_id: int):
    messages_model.nullify_message(message_id)
    return redirect(url_for('admin_person_message', person_id=person_id))

@app.get('/admin/titles/<person_id>')
@login_required
@admin_required
def admin_person_title(person_id: int):
    questions = questions_model.select_where_person(person_id)
    def f(question):
        question['actions'] = ({'label': 'Nullifier',
                'url': url_for('admin_person_title_nullify',
                person_id=person_id, question_id=question['question_id'])}, )
        return question
    questions_with_actions = tuple(map(f, questions))
    return render_template('admin.html', data_list=questions_with_actions,
                           title='Titres des questions')

@app.get('/admin/titles/<person_id>/<question_id>')
@login_required
@admin_required
def admin_person_title_nullify(person_id: int, question_id: int):
    questions_model.nullify_title(question_id)
    return redirect(url_for('admin_person_title', person_id=person_id))
