from sqlalchemy.sql import text
from db import db

def all_artists():
    sql = "SELECT id, name FROM artists ORDER BY name"
    return db.session.execute(text(sql)).fetchall()

def all_albums_from_artist(artist_id):
    sql = """SELECT id, name, artist_id FROM albums
             WHERE artist_id=:artist_id ORDER BY name"""
    return db.session.execute(text(sql), {"artist_id": artist_id}).fetchall()

def all_reviews_for_album(album_id):
    sql = "SELECT id, user_id, score, comment FROM reviews WHERE album_id=:album_id"
    return db.session.execute(text(sql), {"album_id": album_id}).fetchall()

def all_reviews_reversed():
    sql = "SELECT id, user_id, score, comment FROM reviews ORDER BY id DESC"
    return db.session.execute(text(sql)).fetchall()

def artist_info(artist_id):
    sql = "SELECT name, country, year FROM artists WHERE id=:artist_id"
    return db.session.execute(text(sql), {"artist_id": artist_id}).fetchone()

def check_artist_name(artist_name):
    sql = "SELECT name FROM artists WHERE name=:artist_name"
    return db.session.execute(text(sql), {"artist_name": artist_name}).fetchone()

def album_info(album_id):
    sql = "SELECT name, artist_id, year, genre FROM albums WHERE id=:album_id"
    return db.session.execute(text(sql), {"album_id": album_id}).fetchone()

def add_review(user_id, album_id, score, comment):
    sql = """INSERT INTO reviews (user_id, album_id, score, comment)
             VALUES (:user_id, :album_id, :score, :comment)"""
    db.session.execute(text(sql), {"user_id":user_id, "album_id":album_id,
                                   "score":score, "comment":comment})
    db.session.commit()

def add_artist(name, country, year ):
    try:
        sql = """INSERT INTO artists (name, country, year)
                VALUES (:name, :country, :year)"""
        db.session.execute(text(sql), {"name":name, "country":country,
                                    "year":year})
        db.session.commit()
    except:
        return False
    return True

def add_album(name, artist_id, year, genre):
    try:
        sql = """INSERT INTO albums (name, artist_id, year, genre)
                VALUES (:name, :artist_id, :year, :genre)"""
        db.session.execute(text(sql), {"name":name, "artist_id":artist_id,
                                    "year":year, "genre":genre})
        db.session.commit()
    except:
        return False
    return True