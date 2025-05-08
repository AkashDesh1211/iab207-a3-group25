from flask import Blueprint
from flask import render_template, request, redirect, flash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')