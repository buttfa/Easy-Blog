from flask import Flask, render_template
from sqlite3 import connect

app = Flask(__name__)

conn_user = connect('backend/db/user.db')
cursor_user = conn_user.cursor()
conn_post = connect('backend/db/post.db')
cursor_post = conn_post.cursor()

def init_blog():
    pass

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/')