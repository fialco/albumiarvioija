from db import db
from sqlalchemy.sql import text

def all_artists():
    sql = "SELECT id, name FROM artists ORDER BY name"
    return db.session.execute(text(sql)).fetchall()

def artist_info(artist_id):
    sql = "SELECT * FROM artists WHERE id=:artist_id"
    return db.session.execute(text(sql), {"artist_id": artist_id}).fetchone()