from app import app
from flask import Flask
from flask import redirect, render_template, request
import users

from db import db
from sqlalchemy.sql import text


@app.route("/")
def index():
    #result = db.session.execute(text("SELECT content FROM reviews"))
    #reviews = result.fetchall()
    #, reviews=reviews
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        if 1 > len(username) > 20:
            return render_template("error.html", message="Käyttäjätunnuksen tulisi olla 1-20 merkin välillä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        
        rank = request.form["rank"]
        if rank not in ("1", "2", "3"):
            return render_template("error.html", message="Rooli ei kelpaa")
        
        if users.register(username, password1, rank):
            return redirect("/")
        else:
            return render_template("error.html", message="Uuden käyttäjän rekisteröinti ei onnistunut")

    
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")