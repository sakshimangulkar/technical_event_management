from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Product, User, DB
from functools import wraps

vendor_bp = Blueprint('vendor', __name__, template_folder='../templates')


# Decorator to require login
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Login required')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper


@vendor_bp.route('/add_product', methods=['GET','POST'])
@login_required
def add_product():
    user = User.query.get(session['user_id'])

    if user.role != 'vendor':
        flash('Vendor-only page')
        return redirect(url_for('user.products'))

    if request.method == 'POST':
        name = request.form['name']
        desc = request.form.get('desc','')
        price = float(request.form['price'])
        qty = int(request.form['quantity'])

        p = Product(vendor_id=user.id, name=name, description=desc, price=price, quantity=qty)
        DB.session.add(p)
        DB.session.commit()

        flash('Product added')
        return redirect(url_for('user.products'))

    return render_template('add_product.html')
