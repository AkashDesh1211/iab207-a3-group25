from . import db
from datetime import datetime
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    phoneno = db.Column(db.String(100), index=True, nullable=False)
    address = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')

    def get_id(self):
        return (self.user_id)

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(80), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    STEM_category = db.Column(db.Enum("Science", "Information Technology", "Maths", "Engineering"), nullable=False)
    event_type = db.Column(db.Enum("Online", "In-person"))
    event_address = db.Column(db.String(80))
    event_venue = db.Column(db.String(80))
    ticket_price = db.Column(db.Numeric(10,2), nullable=False)
    ticket_policy = db.Column(db.Integer)
    max_num_tickets = db.Column(db.String(100))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    event_status = db.Column(db.Enum("Open", "Inactive", "Sold Out", "Cancelled"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def get_id(self):
        return (self.event_id)

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))