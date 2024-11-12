from flask import Flask, render_template, request, jsonify, session
from sqlite3 import connect
from hashlib import sha256
from getpass import getpass

app = Flask(__name__)

conn_db = None
cursor_db = None

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def init_blog():
    """First, connect to the database and initialize the tables. Secondly, check if there is blogger information in the user table. If not, request to write the relevant information.
    """
    
    # Connect to the database.
    conn_db = connect('backend/db/blog.db')
    conn_db.row_factory = dict_factory # Set the cursor to return the result as a dictionary.
    cursor_db = conn_db.cursor()
    
    # Create tables.
    cursor_db.execute("""
        create table if not exists user (
            id integer primary key autoincrement,
            role text not null,

            name text not null,
                      
            email text not null unique,
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

        # Get blogger's name
        blogger_user_name = input("Please input the name: ")
        
        # Get blogger's email
        blogger_user_email = input("Please input the email: ")

        # Get blogger's password
        blogger_user_password_first = getpass("Please input the password: ")
        blogger_user_password_second = getpass("Please input the password again: ")
        while blogger_user_password_first != blogger_user_password_second:
            blogger_user_password_first = getpass("The passwords do not match. Please input the password again: ")
            blogger_user_password_second = getpass("Please input the password again: ")
        blogger_user_password = blogger_user_password_first

        # Write the blogger information into the user table.
        cursor_db.execute(f"insert into user(role, name, email, password) values('blogger', '{blogger_user_name}', '{blogger_user_email}', '{sha256(blogger_user_password.encode()).hexdigest()}')")
        conn_db.commit()
        print("[Easy-Blog:init]: Succeed to write the blogger information.")

        # Set the secret key of the session.
        cursor_db.execute("SELECT * FROM user WHERE role='blogger'")
        blogger_info = cursor_db.fetchone()
        app.secret_key = blogger_info['name'] + blogger_info['email'] + blogger_info['password']

@app.route('/login', methods=['POST'])
def login():
    user_json_data = request.get_json()
    cursor_db.execute(f"select * from user where email='{user_json_data['email']}' and password='{sha256(user_json_data['password'].encode()).hexdigest()}'")
    user_info = cursor_db.fetchone()
    if user_info is not None:
        session['user_id'] = user_info['id']
        return jsonify({'status': 'success'})
    return jsonify({'status': 'fail'})

@app.route('/get_user_info')
def get_user_info():
    return jsonify({'status': 'fail'})

@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/logout')
def logout():
    return render_template('logout.html')

init_blog()
