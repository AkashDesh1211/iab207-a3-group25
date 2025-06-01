from flask import Blueprint
from flask import render_template, request, redirect, flash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/history')
def history():
    return render_template('booking_history.html')

@main_bp.route('/create')
def create():
    return render_template('create_event.html')

@main_bp.route('/events')
def events():
    return render_template('event_category.html')

@main_bp.route('/details')
def details():
    return render_template('event_details.html')

@main_bp.route('/login')
def login():
    return render_template('login.html')

@main_bp.route('/register')
def register():
    return render_template('register.html')
