# Import database and login/session tools.
from . import db
from datetime import datetime
from flask_login import UserMixin
from datetime import datetime


# User model - stores info about each registered user
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True) # Unique ID for user
    name = db.Column(db.String(100), index=True, unique=True, nullable=False) # Username
    emailid = db.Column(db.String(100), index=True, nullable=False) # User Email
    phoneno = db.Column(db.String(100), index=True, nullable=False) # Contact Number
    address = db.Column(db.String(100), index=True, nullable=False) # User Address
    password_hash = db.Column(db.String(255), nullable=False) # Hashed password (For security purposes)
    comments = db.relationship('Comment', backref='user') # Link to user comments

    def get_id(self):
        return (self.user_id)

# Event model - used to store all event information
class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True) # Unique ID for event
    event_name = db.Column(db.String(80), nullable=False) # Event Name
    start_time = db.Column(db.DateTime, nullable=False) # Start Time 
    end_time = db.Column(db.DateTime, nullable=False) # End Time
    # STEM category dropdown options
    STEM_category = db.Column(db.Enum("Science", "Information Technology", "Maths", "Engineering"), nullable=False) # The Four STEM Fields
    # Event type dropdown options
    event_type = db.Column(db.Enum("Online", "In-Person"), nullable=False) # The Two Event Types
    event_address = db.Column(db.String(80)) # Address for the event (if in-person)
    event_venue = db.Column(db.String(80)) # Venue for the event (if in-person)
    ticket_price = db.Column(db.Numeric(10,2), nullable=False) # Price per ticket
    ticket_policy = db.Column(db.Integer) #Number of tickets per user
    max_num_tickets = db.Column(db.String(100), nullable=False) # Maximum number of tickets available for the event
    description = db.Column(db.String(200)) # Description of the event
    image = db.Column(db.String(400)) # Image URL for the event
    event_status = db.Column(db.Enum("Open", "Inactive", "Sold Out", "Cancelled")) # The Four event statuses
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) # Foreign key to link to the user who created the event
    # A list of comments related to this event
    comments = db.relationship('Comment', backref='event', cascade="all, delete-orphan") 


    def get_id(self):
        return (self.event_id)

# Comment model - links users and events via comment threads
class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True) # Unique ID for comment
    text = db.Column(db.String(400)) # Comment text
    created_at = db.Column(db.DateTime, default=datetime.now()) # Timestamp for when the comment was created
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) # Foreign key to link to the user who made the comment
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id')) # Foreign key to link to the event the comment is related to

# Order model - booking info is stored here
class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True) # Unique ID for order
    created_at = db.Column(db.DateTime, default=datetime.now()) # Timestamp for when the order was created 
    ticket_quantity = db.Column(db.Numeric(10,2)) # Number of tickets ordered
    total_amount = db.Column(db.Integer) # Total amount for the order
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) # Foreign key to link to the user who made the order
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id')) # Foreign key to link to the event the order is for

    event=db.relationship('Event', backref='orders') # Link back to the event