from flask import redirect, render_template, request
from app import app
import users
import artists

@app.route("/")
def index():
    reviews = artists.all_reviews_reversed()
    return render_template("index.html", reviews=reviews)

@app.route("/browse")
def browse():
    return render_template("browse.html", artists=artists.all_artist_info())

@app.route("/artists/<int:artist_id>")
def artist_page(artist_id):
    artist = artists.artist_info(artist_id)
    albums = artists.all_albums_from_artist(artist_id)

    return render_template("artist.html", id=artist_id, name=artist.name, country=artist.country,
                           year=artist.year , albums=albums)

@app.route("/albums/<int:album_id>")
def album_page(album_id):
    album = artists.album_info(album_id)
    artist = artists.artist_info(album.artist_id)
    reviews = artists.all_reviews_for_album(album_id)
    tracks = artists.album_tracks(album_id)
    return render_template("album.html", id=album_id, name=album.name, artist_id=album.artist_id,
                           year=album.year, genre=album.genre , artist_name=artist.name, 
                           reviews=reviews, score=album.score, tracks=tracks)

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

    if artists.check_review(album_id, users.user_id()):
        return render_template("error.html", message="Olet jo kirjoittanut albumille arvion. Poista vanha jos haluat kirjoittaa uuden.")

    artists.add_review(users.user_id(), album_id, score, comment)
    return redirect("/albums/"+str(album_id))

@app.route("/remove_rev/", methods=["POST"])
def remove_review():
    users.check_csrf()
    review_id = request.form["review_id"]
    album_id = artists.album_by_review(review_id)
    artists.remove_review(review_id)
    return redirect("/albums/"+str(album_id[0]))

@app.route("/add_artist", methods=["GET", "POST"])
def add_artist():
    if request.method == "GET":
        return render_template("add_artist.html")

    if request.method == "POST":
        users.check_csrf()
        artist_name = request.form["artist_name"]
        if len(artist_name) < 1 or 50 < len(artist_name):
            return render_template("error.html", message="Nimen tulisi olla 1-50 merkin välillä")
        if artists.check_artist_name(artist_name):
            return render_template("error.html", message=artist_name +" niminen artisti on jo tietokannassa")

        country = request.form["country"]
        if len(country) < 1 or 56 < len(country):
            return render_template("error.html", message="Kotimaan tulisi olla 1-56 merkin välillä")

        year = request.form["year"]
        if int(year) < 1940 or 2023 < int(year):
            return render_template("error.html", message="Vuoden tulisi olla 1940-2023 välillä")

        artists.add_artist(artist_name, country, year)
        return redirect("/browse")

@app.route("/artists/<int:artist_id>/edit_artist", methods=["GET", "POST"])
def edit_artist(artist_id):
    if request.method == "GET":
        artist = artists.artist_info(artist_id)
        return render_template("edit_artist.html", id=artist_id, name=artist.name,
                           year=artist.year, country=artist.country)

    if request.method == "POST":
        users.check_csrf()
        artist = artists.artist_info(artist_id)
        artist_name = request.form["artist_name"]
        if len(artist_name) < 1 or 50 < len(artist_name):
            return render_template("error.html", message="Nimen tulisi olla 1-50 merkin välillä")
        if artists.check_artist_name(artist_name) and artist_name != artist.name:
            return render_template("error.html", message=artist_name +" niminen artisti on jo tietokannassa")

        country = request.form["country"]
        if len(country) < 1 or 56 < len(country):
            return render_template("error.html", message="Kotimaan tulisi olla 1-56 merkin välillä")

        year = request.form["year"]
        if int(year) < 1940 or 2023 < int(year):
            return render_template("error.html", message="Vuoden tulisi olla 1940-2023 välillä")

        artists.edit_artist(artist_id, artist_name, country, year)
        return redirect("/artists/"+str(artist_id))

@app.route("/artists/<int:artist_id>/delete_artist", methods=["POST"])
def delete_artist(artist_id):
    albums = artists.all_albums_from_artist(artist_id)
    
    for album in albums:
        artists.delete_tracks(album.id)
        artists.delete_reviews(album.id)

    artists.delete_albums(artist_id)
    artists.delete_artist(artist_id)
    
    return redirect("/browse")

@app.route("/artists/<int:artist_id>/add_album", methods=["GET", "POST"])
def add_album(artist_id):
    if request.method == "GET":
        artist = artists.artist_info(artist_id)
        albums = artists.all_albums_from_artist(artist_id)
        return render_template("add_album.html", artist_id=artist_id, artist_name=artist.name,
                           artist_year=artist.year, albums=albums)

    if request.method == "POST":
        users.check_csrf()
        album_name = request.form["album_name"]
        name_check = artists.check_name(artist_id, album_name)
        if len(album_name) < 1 or 50 < len(album_name):
            return render_template("error.html", message="Nimen tulisi olla 1-50 merkin välillä")

        if name_check:
            return render_template("error.html", message="Artistilla on jo saman niminen albumi tietokannassa")

        year = request.form["year"]
        if int(year) < 1940 or 2023 < int(year):
            return render_template("error.html", message="Vuoden tulisi olla 1940-2023 välillä")

        genre = request.form["genre"]
        if len(genre) < 1 or 50 < len(genre):
            return render_template("error.html", message="Genren tulisi olla 1-50 merkin välillä")

        track_name = request.form.getlist("track_name")
        track_length = request.form.getlist("track_length")

        album_id = artists.add_album(album_name, artist_id, year, genre)

        for i in range(len(track_name)):       
            artists.add_tracks(artist_id, album_id[0], track_name[i], track_length[i])

        return redirect("/artists/"+str(artist_id))

@app.route("/albums/<int:album_id>/edit_album", methods=["GET", "POST"])
def edit_album(album_id):
    if request.method == "GET":
        album = artists.album_info(album_id)
        artist = artists.artist_info(album.artist_id)
        tracks = artists.album_tracks(album_id)
        return render_template("edit_album.html", id=album_id, name=album.name,
                           year=album.year, genre=album.genre, artist_year=artist.year, tracks=tracks)

    if request.method == "POST":
        users.check_csrf()

        album = artists.album_info(album_id)
        artist = artists.artist_info(album.artist_id)
        tracks = artists.album_tracks(album_id)

        album_name = request.form["album_name"]
        name_check = artists.check_name(artist.id, album_name)
        if len(album_name) < 1 or 50 < len(album_name):
            return render_template("error.html", message="Nimen tulisi olla 1-50 merkin välillä")

        if name_check:
            if album_name.lower() != name_check[0]:
                return render_template("error.html", message="Artistilla on jo saman niminen albumi tietokannassa")

        year = request.form["year"]
        if int(year) < 1940 or 2023 < int(year):
            return render_template("error.html", message="Vuoden tulisi olla 1940-2023 välillä")

        genre = request.form["genre"]
        if len(genre) < 1 or 56 < len(genre):
            return render_template("error.html", message="Kotimaan tulisi olla 1-56 merkin välillä")

        track_name = request.form.getlist("track_name")
        track_length = request.form.getlist("track_length")

        artists.edit_album(album_id, album_name, year, genre)

        #Tracks are updated
        if len(track_name) == len(tracks):
            print("kel")
            for i in range(len(track_name)):       
                artists.edit_tracks(tracks[i].id, track_name[i], track_length[i])
        #If track amount differs after editing, tracks are deleted and added again
        else:
            artists.delete_tracks(album_id)
            for i in range(len(track_name)):       
                artists.add_tracks(artist.id, album_id, track_name[i], track_length[i])

        return redirect("/albums/"+str(album_id))

@app.route("/albums/<int:album_id>/delete_album", methods=["POST"])
def delete_album(album_id):
    album = artists.album_info(album_id)
    artists.delete_album(album_id)
    artists.delete_tracks(album_id)
    artists.delete_reviews(album_id)
    return redirect("/artists/"+str(album.artist_id))

@app.route("/search")
def search():
        query = request.args["query"]
        result = artists.search(query)
        return render_template("search.html", query=result)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        users.check_csrf()
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
        return render_template("error.html", message="Uuden käyttäjän rekisteröinti ei onnistunut")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")
