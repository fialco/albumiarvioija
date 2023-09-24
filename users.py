import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def login(username, password):
    sql = "SELECT id, password, rank FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["user_rank"] = user.rank
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def register(username, password, rank):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, rank) VALUES (:username, :password, :rank)"
        db.session.execute(text(sql), {"username":username, "password":hash_value, "rank":rank})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]
    del session["username"]
    del session["user_rank"]

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
        
def user_id():
    return session.get("user_id", 0)