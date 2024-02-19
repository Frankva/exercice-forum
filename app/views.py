from .models import questions as questionsModel
from .models.tags import formatTags
from flask import Flask, render_template, request
app = Flask(__name__)
app.config.from_object('config')
import sys


@app.route('/')
def index():
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
    question = questionsModel.select_one(id)[0]
    question['id'] = id
    return render_template('question.html', question=question)

@app.post('/question/<id>')
def question_post(id):
    print(request.form['answer'], file=sys.stderr)
    return question_get(id)

    

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
