from db import db
from sqlalchemy.sql import text

def all_artists():
    sql = "SELECT id, name FROM artists ORDER BY name"
    return db.session.execute(text(sql)).fetchall()

def all_albums_from_artist(artist_id):
    sql = "SELECT id, name, artist_id FROM albums WHERE artist_id=:artist_id ORDER BY name"
    return db.session.execute(text(sql), {"artist_id": artist_id}).fetchall()

def artist_info(artist_id):
    sql = "SELECT * FROM artists WHERE id=:artist_id"
    return db.session.execute(text(sql), {"artist_id": artist_id}).fetchone()

def album_info(album_id):
    sql = "SELECT * FROM albums WHERE id=:album_id"
    return db.session.execute(text(sql), {"album_id": album_id}).fetchone()