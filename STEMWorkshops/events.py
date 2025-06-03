from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment
from .forms import EventsForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user


events_bp = Blueprint('main', __name__)

@events_bp.route('/create')
@login_required
def create():
    return render_template('create_event.html')