from flask import Flask, render_template, request
app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/question')
def question():
    return render_template('question.html')

@app.get('/ask')
def getAsk():
    return render_template('ask.html')

@app.post('/ask')
def postAsk():
    print(request.form['title'])
    print(request.form['body'])
    print(request.form['tags'])
    return render_template('ask.html')
