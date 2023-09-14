from app import app
from flask import Flask
from flask import redirect, render_template, request


from db import db
from sqlalchemy.sql import text


@app.route("/")
def index():
    result = db.session.execute(text("SELECT content FROM messages"))
    messages = result.fetchall()
    return render_template("index.html", messages=messages)