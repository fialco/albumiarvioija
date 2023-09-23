from app import app
from flask import Flask
from flask import redirect, render_template, request
import users
import artists

from db import db
from sqlalchemy.sql import text


@app.route("/")
def index():
    #result = db.session.execute(text("SELECT content FROM reviews"))
    #reviews = result.fetchall()
    #, reviews=reviews
    return render_template("index.html")

@app.route("/browse")
def browse():
    #result = db.session.execute(text("SELECT content FROM reviews"))
    #reviews = result.fetchall()
    #, reviews=reviews
    return render_template("browse.html", artists=artists.all_artists())

@app.route("/artists/<int:artist_id>")
def artist_page(artist_id):
    artist = artists.artist_info(artist_id)
    albums = artists.all_albums_from_artist(artist_id)
    return render_template("artist.html", id=artist_id, name=artist.name, country=artist.country, year=artist.year, genre=artist.genre, albums=albums)

@app.route("/albums/<int:album_id>")
def album_page(album_id):
    album = artists.album_info(album_id)
    artist = artists.artist_info(album.artist_id)
    return render_template("album.html", id=album_id, name=album.name, artist_id=album.artist_id, year=album.year, artist_name=artist.name)

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