from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)