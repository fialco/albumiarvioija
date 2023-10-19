from sqlalchemy.sql import text
from db import db

def all_artist_info():
    sql = """SELECT a.id, a.name, a.country, a.year, COUNT(distinct b.id) AS album_count, COUNT(distinct t.id) AS track_count FROM artists a
            LEFT JOIN albums b ON a.id=b.artist_id
            LEFT JOIN tracks t ON a.id=t.artist_id GROUP BY a.id ORDER BY a.name"""
    return db.session.execute(text(sql)).fetchall()

def all_albums_from_artist(artist_id):
    sql = """SELECT a.id, a.name, a.artist_id, a.year, a.genre, ROUND(AVG(r.score), 2) AS score FROM albums a
            LEFT JOIN reviews r ON a.id=r.album_id WHERE a.artist_id=:artist_id
            GROUP BY a.id ORDER BY a.year"""
    return db.session.execute(text(sql), {"artist_id": artist_id}).fetchall()

def check_name(artist_id, name):
    sql = "SELECT LOWER(name) FROM albums WHERE artist_id=:artist_id AND LOWER(name)=LOWER(:name)"
    return db.session.execute(text(sql), {"artist_id": artist_id, "name": name}).fetchone()

def check_review(album_id, user_id):
    sql = "SELECT id FROM reviews WHERE album_id=:album_id AND user_id=:user_id"
    return db.session.execute(text(sql), {"album_id": album_id, "user_id": user_id}).fetchone()


def all_reviews_for_album(album_id):
    sql = """SELECT r.id AS review_id, r.score, r.comment, r.created, r.user_id, u.username FROM reviews r
            LEFT JOIN users u ON r.user_id=u.id WHERE r.album_id=:album_id ORDER BY r.created"""
    return db.session.execute(text(sql), {"album_id": album_id}).fetchall()

def all_reviews_reversed():
    sql = """SELECT r.score, r.comment, r.created, a.id, a.name, u.username FROM reviews r
            LEFT JOIN albums a ON r.album_id=a.id
            LEFT JOIN users u ON r.user_id=u.id ORDER BY r.created DESC LIMIT 8"""
    return db.session.execute(text(sql)).fetchall()


def artist_info(artist_id):
    sql = "SELECT id, name, country, year FROM artists WHERE id=:artist_id"
    return db.session.execute(text(sql), {"artist_id": artist_id}).fetchone()

def check_artist_name(artist_name):
    sql = "SELECT name FROM artists WHERE name=:artist_name"
    return db.session.execute(text(sql), {"artist_name": artist_name}).fetchone()

def album_info(album_id):
    sql = """SELECT a.name, a.artist_id, a.year, a.genre, ROUND(AVG(r.score), 2) AS score FROM albums a
            LEFT JOIN reviews r ON a.id=r.album_id WHERE a.id=:album_id GROUP BY a.id"""
    return db.session.execute(text(sql), {"album_id": album_id}).fetchone()

def album_tracks(album_id):
    sql = "SELECT id, artist_id, album_id, name, length FROM tracks WHERE album_id=:album_id"
    return db.session.execute(text(sql), {"album_id": album_id}).fetchall()


def add_review(user_id, album_id, score, comment):
    sql = """INSERT INTO reviews (user_id, album_id, score, comment, created)
             VALUES (:user_id, :album_id, :score, :comment, NOW())"""
    db.session.execute(text(sql), {"user_id":user_id, "album_id":album_id,
                                   "score":score, "comment":comment})
    db.session.commit()

def remove_review(id):
    sql = "DELETE FROM reviews WHERE id=:id"
    db.session.execute(text(sql), {"id": id})
    db.session.commit()

def delete_reviews(album_id):
    sql = "DELETE FROM reviews WHERE album_id=:album_id"
    db.session.execute(text(sql), {"album_id": album_id})
    db.session.commit()

def album_by_review(id):
    sql = "SELECT album_id FROM reviews WHERE id=:id"
    db.session.execute(text(sql), {"id": id})
    return db.session.execute(text(sql), {"id": id}).fetchone()


def add_artist(name, country, year):
    sql = """INSERT INTO artists (name, country, year)
            VALUES (:name, :country, :year)"""
    db.session.execute(text(sql), {"name":name, "country":country,
                                "year":year})
    db.session.commit()

def edit_artist(id, name, country, year):
    sql = """UPDATE artists SET (name, country, year) =
            (:name, :country, :year) WHERE id=:id"""
    db.session.execute(text(sql), {"id":id, "name":name,
    "country":country, "year":year})
    db.session.commit()

def delete_artist(id):
    sql = "DELETE FROM artists WHERE id=:id"
    db.session.execute(text(sql), {"id": id})
    db.session.commit()


def add_album(name, artist_id, year, genre):
    sql = """INSERT INTO albums (name, artist_id, year, genre)
            VALUES (:name, :artist_id, :year, :genre) RETURNING albums.id"""
    id = db.session.execute(text(sql), {"name":name, "artist_id":artist_id,
                                "year":year, "genre":genre})
    db.session.commit()
    return id.fetchone()

def edit_album(id, name, year, genre):
    sql = """UPDATE albums SET (name, year, genre) =
            (:name, :year, :genre) WHERE id=:id"""
    db.session.execute(text(sql), {"id":id, "name":name,
    "year":year, "genre":genre})
    db.session.commit()

def delete_album(id):
    sql = "DELETE FROM albums WHERE id=:id"
    db.session.execute(text(sql), {"id": id})
    db.session.commit()

def delete_albums(artist_id):
    sql = "DELETE FROM albums WHERE artist_id=:artist_id"
    db.session.execute(text(sql), {"artist_id": artist_id})
    db.session.commit()


def add_tracks(artist_id, album_id, name, length):
    sql = """INSERT INTO tracks (artist_id, album_id, name, length)
            VALUES (:artist_id, :album_id, :name, :length)"""
    db.session.execute(text(sql), {"artist_id":artist_id, "album_id":album_id,
                                "name":name, "length":length})
    db.session.commit()

def edit_tracks(id, name, length):
    sql = """UPDATE tracks SET (name, length) =
            (:name, :length) WHERE id=:id"""
    db.session.execute(text(sql), {"id":id, "name":name, "length":length})
    db.session.commit()

def delete_tracks(album_id):
    sql = "DELETE FROM tracks WHERE album_id=:album_id"
    db.session.execute(text(sql), {"album_id": album_id})
    db.session.commit()


def search(query):
    sql = """SELECT a.id AS artist_id, a.name AS artist, b.id AS album_id, b.name AS album FROM artists a
            LEFT JOIN albums b ON a.id=b.artist_id WHERE LOWER(a.name)
            LIKE LOWER(:query) OR LOWER(b.name) LIKE LOWER(:query)"""
    return db.session.execute(text(sql), {"query":"%"+query+"%"}).fetchall()
