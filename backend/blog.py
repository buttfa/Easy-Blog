from flask import Flask, request, jsonify, session
from flask_cors import CORS
from sqlite3 import Connection, Cursor, connect
from hashlib import sha256
from getpass import getpass

app = Flask(__name__)
CORS(app, supports_credentials=True)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_db() -> tuple[Connection, Cursor]:
    """Initialize the database."""
    # Connect to the database.
    conn_db = connect("backend/db/blog.db")
    conn_db.row_factory = (
        dict_factory  # Set the cursor to return the result as a dictionary.
    )
    cursor_db = conn_db.cursor()

    # Create tables.
    cursor_db.execute("""
        create table if not exists user (
            user_id integer primary key autoincrement,
            role text not null,

            name text not null,
                      
            email text not null unique,
            password text not null,
                      
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor_db.execute("""
        create table if not exists post (
            post_id integer primary key autoincrement,
            
            title text not null,
            author text not null,
            content text not null,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor_db.execute("""
        create table if not exists comment (
            comment_id integer primary key autoincrement,
            
            user_id integer not null,
            post_id integer not null,
            content text not null,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      
            foreign key(user_id) references user(user_id),
            foreign key(post_id) references post(post_id)
        )
    """)

    # Check if there is blogger information in the user table.
    cursor_db.execute("SELECT * FROM user WHERE role='blogger'")
    blogger_info = cursor_db.fetchone()
    if blogger_info is None:
        print(
            "[Easy-Blog:init]: There is no blogger information in the user table. Please write the blogger information."
        )

        # Get blogger's name
        blogger_user_name = input("Please input the name: ")

        # Get blogger's email
        blogger_user_email = input("Please input the email: ")

        # Get blogger's password
        blogger_user_password_first = getpass("Please input the password: ")
        blogger_user_password_second = getpass("Please input the password again: ")
        while blogger_user_password_first != blogger_user_password_second:
            blogger_user_password_first = getpass(
                "The passwords do not match. Please input the password again: "
            )
            blogger_user_password_second = getpass("Please input the password again: ")
        blogger_user_password = blogger_user_password_first

        # Write the blogger information into the user table.
        cursor_db.execute(
            f"insert into user(role, name, email, password) values('blogger', '{blogger_user_name}', '{blogger_user_email}', '{sha256(blogger_user_password.encode()).hexdigest()}')"
        )
        conn_db.commit()
        print("[Easy-Blog:init]: Succeed to write the blogger information.")

    # Set the secret key of the session.
    cursor_db.execute("SELECT * FROM user WHERE role='blogger'")
    blogger_info = cursor_db.fetchone()
    app.secret_key = (
        blogger_info["name"] + blogger_info["email"] + blogger_info["password"]
    )

    return conn_db, cursor_db


def close_db(conn_db: Connection, cursor_db: Cursor):
    """Close the database."""
    if cursor_db is not None:
        cursor_db.close()

    if conn_db is not None:
        conn_db.close()


def init_blog():
    """First, connect to the database and initialize the tables. Secondly, check if there is blogger information in the user table. If not, request to write the relevant information."""
    # Initialize the database and write the blogger information.
    conn_db, cursor_db = init_db()
    close_db(conn_db, cursor_db)


@app.route("/login", methods=["POST"])
def login():
    # Connect to the database.
    conn_db, cursor_db = init_db()

    # Get the user login information in jsn format
    user_json_data = request.get_json()

    # Check if the user exists.
    cursor_db.execute(
        f"select * from user where email='{user_json_data['email']}' and password='{sha256(user_json_data['password'].encode()).hexdigest()}'"
    )
    user_info = cursor_db.fetchone()

    # If the user exists, return the {'status': 'success'}
    if user_info is not None:
        session["user_id"] = user_info["user_id"]
        close_db(conn_db, cursor_db)
        return jsonify({"status": "success"})

    # If the user does not exist, return the {'status': 'fail'}
    close_db(conn_db, cursor_db)
    return jsonify({"status": "fail"})


@app.route("/get_blogger_info", methods=["POST"])
def get_blogger_info():
    conn_db, cursor_db = init_db()
    cursor_db.execute("select * from user where role='blogger'")
    blogger_info = cursor_db.fetchone()
    return jsonify({"status": "success", "blogger_info": blogger_info})


@app.route("/get_user_info", methods=["POST"])
def get_user_info():
    conn_db, cursor_db = init_db()

    user_id = session.get("user_id")

    # Check if the user is logged in.
    if user_id is None:
        return jsonify({"status": "fail"})

    # Return the user information. (except the password)
    cursor_db.execute(f"select * from user where user_id={user_id}")
    user_info = cursor_db.fetchone()
    user_info.pop("password")
    return jsonify({"status": "success", "user_info": user_info})


@app.route("/register", methods=["POST"])
def register():
    conn_db, cursor_db = init_db()
    user_json_data = request.get_json()

    # Check if the email is already registered.
    cursor_db.execute(f"select * from user where email='{user_json_data['email']}'")
    user_info = cursor_db.fetchone()
    if user_info is not None:
        close_db(conn_db, cursor_db)
        return jsonify({"status": "fail"})

    # Register the user.
    cursor_db.execute(
        f"insert into user(role, name, email, password) values('visitor', '{user_json_data['name']}', '{user_json_data['email']}', '{sha256(user_json_data['password'].encode()).hexdigest()}')"
    )
    conn_db.commit()
    return jsonify({"status": "success"})


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"status": "success"})


@app.route("/get_post_list", methods=["POST"])
def get_post_list():
    conn_db, cursor_db = init_db()

    # Get all the post information
    cursor_db.execute("select * from post")
    post_list = cursor_db.fetchall()
    # Only show the first 200 characters of the content
    for post in post_list:
        post["content"] = post["content"][:200]

    close_db(conn_db, cursor_db)
    return jsonify({"status": "success", "post_list": post_list})


@app.route("/get_post_info", methods=["POST"])
def get_post_info():
    conn_db, cursor_db = init_db()

    # Get the target post id
    post_json_data = request.get_json()
    cursor_db.execute(f"select * from post where post_id='{post_json_data['post_id']}'")
    post_info = cursor_db.fetchone()

    # Check if the post exists
    if post_info is None:
        close_db(conn_db, cursor_db)
        return jsonify({"status": "fail"})

    close_db(conn_db, cursor_db)
    return jsonify({"status": "success", "post_info": post_info})


@app.route("/add_post", methods=["POST"])
def add_post():
    conn_db, cursor_db = init_db()

    user_id = session.get("user_id")
    # Check if the user is logged in.
    if user_id is None:
        close_db(conn_db, cursor_db)
        return jsonify({"status": "fail"})

    # Check if the user is blogger.
    cursor_db.execute(f"select * from user where user_id={user_id}")
    user_info = cursor_db.fetchone()
    if user_info is None or (
        user_info["role"] != "blogger" and user_info["role"] != "manager"
    ):
        close_db(conn_db, cursor_db)
        return jsonify({"status": "fail"})

    # Get the post information in json format and add the post.
    post_json_data = request.get_json()
    cursor_db.execute(
        f"insert into post(title, author, content) values('{post_json_data['title']}', '{post_json_data['author']}', '{post_json_data['content']}')"
    )
    conn_db.commit()

    close_db(conn_db, cursor_db)
    return jsonify({"status": "success"})


@app.route("/delete_post", methods=["POST"])
def delete_post():
    conn_db, cursor_db = init_db()

    # Get the target user id
    user_id = session.get("user_id")
    # Check if the user is logged in.
    if user_id is None:
        close_db(conn_db, cursor_db)
        return jsonify({"status": "fail"})

    # Check if the user is blogger or manager.
    cursor_db.execute(f"select * from user where user_id={user_id}")
    user_info = cursor_db.fetchone()
    if user_info is None or (
        user_info["role"] != "blogger" and user_info["role"] != "manager"
    ):
        close_db(conn_db, cursor_db)
        return jsonify({"status": "fail"})

    # Get the post information in json format and delete the post.
    post_json_data = request.get_json()
    cursor_db.execute(f"delete from post where post_id={post_json_data['post_id']}")
    conn_db.commit()

    close_db(conn_db, cursor_db)
    return jsonify({"status": "success"})


@app.route("/update_post_info", methods=["POST"])
def update_post_info():
    conn_db, cursor_db = init_db()

    user_id = session.get("user_id")
    # Check if the user is logged in.
    if user_id is None:
        close_db(conn_db, cursor_db)
        return jsonify({"status": "fail"})

    # Check if the user is blogger or manager.
    cursor_db.execute(f"select * from user where user_id={user_id}")
    user_info = cursor_db.fetchone()
    if user_info is None or (
        user_info["role"] != "blogger" and user_info["role"] != "manager"
    ):
        close_db(conn_db, cursor_db)
        return jsonify({"status": "fail"})

    # Get the post information in json format and update the post.
    post_json_data = request.get_json()
    cursor_db.execute(
        f"update post set title='{post_json_data['title']}', author='{post_json_data['author']}', content='{post_json_data['content']}' where post_id={post_json_data['post_id']}"
    )
    conn_db.commit()
    close_db(conn_db, cursor_db)
    return jsonify({"status": "success"})


@app.route("/get_comment_list", methods=["POST"])
def get_comment_list():
    conn_db, cursor_db = init_db()

    post_json_data = request.get_json()
    cursor_db.execute(
        f"select * from comment where post_id={post_json_data['post_id']}"
    )
    comment_list = cursor_db.fetchall()

    # Add corresponding user names to each comment.
    for comment in comment_list:
        # Obtain username through user_id.
        cursor_db.execute(f"select * from user where user_id='{comment['user_id']}'")
        user_info = cursor_db.fetchone()
        comment["name"] = user_info["name"]

    close_db(conn_db, cursor_db)
    return jsonify({"status": "success", "comment_list": comment_list})


@app.route("/add_comment", methods=["POST"])
def add_comment():
    conn_db, cursor_db = init_db()

    user_id = session.get("user_id")
    # Check if the user is logged in.
    if user_id is None:
        close_db(conn_db, cursor_db)
        return jsonify({"status": "fail"})

    comment_json_data = request.get_json()
    cursor_db.execute(
        f"insert into comment(post_id, user_id, content) values({comment_json_data['post_id']}, {user_id}, '{comment_json_data['content']}')"
    )
    conn_db.commit()
    close_db(conn_db, cursor_db)
    return jsonify({"status": "success"})


init_blog()
