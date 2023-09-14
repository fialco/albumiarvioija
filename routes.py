from app import app
from flask import Flask
from flask import redirect, render_template, request

@app.route("/")
def index():
    return render_template("index.html")