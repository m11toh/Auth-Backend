from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import uuid

db = SQLAlchemy()

def get_uuid():
    return uuid.uuid4().hex


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, unique=True,default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.String(255), nullable=False)