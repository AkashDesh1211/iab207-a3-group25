from flask import Blueprint
from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/history')
@login_required
def history():
    return render_template('booking_history.html')

@main_bp.route('/create')
@login_required
def create():
    return render_template('create_event.html')

@main_bp.route('/events')
def events():
    return render_template('event_category.html')

@main_bp.route('/details')
def details():
    return render_template('event_details.html')

