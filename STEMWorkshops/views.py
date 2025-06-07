from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, Order
from .forms import EventsForm, CommentsForm, OrdersForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime
from .events import get_all_events_ordered_by_status

main_bp = Blueprint('main', __name__)

# Route for homepage
@main_bp.route('/')
def index():
    category = request.args.get('category')
    status = request.args.get('status')
    time = request.args.get('time')
    event_type = request.args.get('event_type')

    # If no filters, show all events sorted by status.
    if not category and not status and not time and not event_type:
        events = get_all_events_ordered_by_status()
    else:
        events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events=events, category=category, status=status, time=time, event_type=event_type, now=datetime.now)





