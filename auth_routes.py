from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import User, DB
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/')
def home():
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # handle login logic
        return redirect(url_for('auth_bp.home'))
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # handle registration logic
        return redirect(url_for('auth_bp.login'))
    return render_template('register.html')
