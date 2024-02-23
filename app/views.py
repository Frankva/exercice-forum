from .models import questions as questionsModel
from .models.tags import formatTags
from .models import tags as tagsModel
from flask import Flask, render_template, request
app = Flask(__name__)
app.config.from_object('config')
import sys
from .models import answers as answersModel


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
    question, tags = questionsModel.select_one(id)
    
    question['id'] = id
    answers = answersModel.select(id)
    print(answers, file=sys.stderr)
    print(type(answers), file=sys.stderr)
    return render_template('question.html', question=question, answers=answers,
                           tags=tags)

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
