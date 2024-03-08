from .models import questions as questionsModel
from .models.tags import formatTags
from .models import tags as tagsModel
from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)
app.config.from_object('config')
import sys
from .models import answers as answersModel
from .models import votes as votesModel

from flask import session

app.secret_key = app.config['SECRET_KEY']

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.get('/questions')
def questions_get():
    questions = questionsModel.select()
    return render_template('questions.html', questions=questions)

@app.get('/question/<id>')
def question_get(id):
    question, tags, vote, uservote = questionsModel.select_one(id, 1)
    # TODO
    # above change the 1 when implement session
    
    question['id'] = id
    answers = answersModel.select(id, 1)
    # TODO
    # above change the 1 when implement session
    print(answers, file=sys.stderr)
    print(type(answers), file=sys.stderr)
    return render_template('question.html', question=question, answers=answers,
                           tags=tags, vote=vote, uservote=uservote)

@app.post('/question/<int:id>')
def question_post(id):
    print(request.form['answer'], file=sys.stderr)
    answersModel.insert(text=request.form['answer'],
                         person_id=1,
                         question_id=id)
    # TODO
    # above change the 1 when implement session
    
    return question_get(id)

@app.route('/questions/tagged/<tag>')
def tagged_questions(tag):
    questions = questionsModel.select_where_tag(tag)
    return render_template('questions.html', questions=questions)

    

@app.get('/ask')
def ask_get():
    return render_template('ask.html')

@app.post('/ask')
def ask_post():
    print(request.form['title'])
    print(request.form['body'])
    print(request.form['tags'])
    questionsModel.insert(title=request.form['title'],
                     body=request.form['body'],
                     tags=formatTags(request.form['tags']),
                     user_id=1)
    # TODO
    # above change the 1 when implement session
    return ask_get()

@app.route('/tags')
def tags():
    tags = tagsModel.select_all()
    return render_template('tags.html', tags=tags)

@app.post('/upvote')
def upvote():
    print(request.get_json(), file=sys.stderr)
    message_id = request.json['messageId'] 
    votesModel.insert_vote(is_upvote=True, person_id=1, message_id=message_id)
    # TODO
    # above change the 1 when implement session
    return jsonify({"message":"Ok"})
    

@app.post('/downvote')
def downvote():
    print(request.get_json(), file=sys.stderr)
    message_id = request.json['messageId'] 
    votesModel.insert_vote(is_upvote=False, person_id=1, message_id=message_id)
    # TODO
    # above change the 1 when implement session
    return jsonify({"message":"Ok"})

@app.post('/nullify-vote')
def nullify_vote():
    print(request.get_json(), file=sys.stderr)
    message_id = request.json['messageId'] 
    votesModel.delete_vote(person_id=1, message_id=message_id)
    # TODO
    # above change the 1 when implement session
    return jsonify({"message":"Ok"})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')
    # return '''
    #     <form method="post">
    #         <p><input type=text name=username>
    #         <p><input type=submit value=Login>
    #     </form>
    # '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

