from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment
from .forms import EventsForm, CommentsForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events=events)

@main_bp.route('/history')
@login_required
def history():
    return render_template('booking_history.html')

@main_bp.route('/events')
def events():
    return render_template('event_category.html')


