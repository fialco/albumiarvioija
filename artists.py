from db import db
from sqlalchemy.sql import text

def all_artists():
    sql = "SELECT id, name FROM artists ORDER BY name"
    return db.session.execute(text(sql)).fetchall()