from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User, DB  # Import DB here as well

auth_bp = Blueprint('auth', __name__, template_folder='../templates')


@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'user')

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))

        u = User(name=name, email=email, role=role)
        u.set_password(password)
        DB.session.add(u)
        DB.session.commit()

        flash('Registered. Please login.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        u = User.query.filter_by(email=email).first()
        if not u or not u.check_password(password):
            flash('Invalid credentials')
            return redirect(url_for('auth.login'))

        session['user_id'] = u.id
        flash('Logged in')
        return redirect(url_for('user.products'))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out')
    return redirect(url_for('auth.login'))
