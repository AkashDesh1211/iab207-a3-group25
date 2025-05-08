from flask import Blueprint
from flask import render_template, request, redirect, flash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/history')
def index():
    return render_template('booking_history.html')

@main_bp.route('/create')
def index():
    return render_template('create_event.html')

@main_bp.route('/events')
def index():
    return render_template('event_category.html')

@main_bp.route('/details')
def index():
    return render_template('event_details.html')