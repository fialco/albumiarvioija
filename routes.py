from app import app
from flask import Flask
from flask import redirect, render_template, request
import users
import artists

@app.route("/")
def index():
    reviews = artists.all_reviews_reversed()
    return render_template("index.html", reviews=reviews)

@app.route("/browse")
def browse():
    return render_template("browse.html", artists=artists.all_artists())

@app.route("/artists/<int:artist_id>")
def artist_page(artist_id):
    artist = artists.artist_info(artist_id)
    albums = artists.all_albums_from_artist(artist_id)

    return render_template("artist.html", id=artist_id, name=artist.name, country=artist.country, 
                           year=artist.year, genre=artist.genre, albums=albums)

@app.route("/albums/<int:album_id>")
def album_page(album_id):
    album = artists.album_info(album_id)
    artist = artists.artist_info(album.artist_id)
    reviews = artists.all_reviews_for_album(album_id)

    return render_template("album.html", id=album_id, name=album.name, artist_id=album.artist_id, 
                           year=album.year, artist_name=artist.name, reviews=reviews)

@app.route("/review/", methods=["POST"])
def review():
    users.check_csrf()
    album_id = request.form["album_id"]

    score = int(request.form["score"])
    if score < 1 or 5 < score:
        return render_template("error.html", message="Pistemäärä ei kelpaa")

    comment = request.form["comment"]
    if len(comment) > 1000:
        return render_template("error.html", message="Kommentti on liian pitkä")
    if comment == "":
        return render_template("error.html", message="Kommenttikenttä on tyhjä")

    artists.add_review(users.user_id(), album_id, score, comment)
    return redirect("/albums/"+str(album_id))


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
        if len(username) < 1 or 20 < len(username):
            return render_template("error.html", message="Käyttäjätunnuksen tulisi olla 1-20 merkin välillä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät ole samat")
        
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