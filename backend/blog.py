from flask import Flask, render_template
from sqlite3 import connect
from hashlib import sha256

app = Flask(__name__)

conn_db = None
cursor_db = None

def init_blog():
    """First, connect to the database and initialize the tables. Secondly, check if there is blogger information in the user table. If not, request to write the relevant information.
    """
    
    # Connect to the database.
    conn_db = connect('backend/db/blog.db')
    cursor_db = conn_db.cursor()

    # Create tables.
    cursor_db.execute("""
        create table if not exists user (
            id integer primary key autoincrement,
            role text not null,

            username text not null,
                      
            email text not null,
            password text not null,
                      
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor_db.execute("""
        create table if not exists post (
            id integer primary key autoincrement,
            
            title text not null,
            author text not null,
            content text not null,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor_db.execute("""
        create table if not exists comment (
            id integer primary key autoincrement,
            
            user_id integer not null,
            post_id integer not null,
            content text not null,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check if there is blogger information in the user table.
    cursor_db.execute("SELECT * FROM user WHERE role='blogger'")
    blogger_info = cursor_db.fetchone()
    if blogger_info is None:
        print("[Easy-Blog:init]: There is no blogger information in the user table. Please write the blogger information.")

        blogger_user_name = input("Please input the username: ")
        blogger_user_email = input("Please input the email: ")
        blogger_user_password = input("Please input the password: ")

        cursor_db.execute(f"insert into user(role, username, email, password) values('blogger', '{blogger_user_name}', '{blogger_user_email}', '{sha256(blogger_user_password.encode()).hexdigest()}')")
        conn_db.commit()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

init_blog()
