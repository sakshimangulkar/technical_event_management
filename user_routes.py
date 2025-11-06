from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Product, CartItem, Order, OrderItem, DB, User
from functools import wraps

user_bp = Blueprint('user', __name__, template_folder='../templates')


# Decorator to require login
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Login required')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper


# Helper to get current logged-in user
def current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


@user_bp.route('/products')
def products():
    prods = Product.query.all()
    user = current_user()
    return render_template('products.html', prods=prods, user=user)


@user_bp.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    user = current_user()
    pid = int(request.form['product_id'])
    qty = int(request.form.get('qty', 1))
    p = Product.query.get(pid)

    if not p or p.quantity < qty:
        flash('Not enough stock')
        return redirect(url_for('user.products'))

    ci = CartItem.query.filter_by(user_id=user.id, product_id=pid).first()
    if ci:
        ci.qty += qty
    else:
        ci = CartItem(user_id=user.id, product_id=pid, qty=qty)
        DB.session.add(ci)

    DB.session.commit()
    flash('Added to cart')
    return redirect(url_for('user.products'))


@user_bp.route('/cart')
@login_required
def cart():
    user = current_user()
    items = CartItem.query.filter_by(user_id=user.id).all()
    total = sum(i.product.price * i.qty for i in items)
    return render_template('cart.html', items=items, total=total)


@user_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    user = current_user()
    items = CartItem.query.filter_by(user_id=user.id).all()

    if not items:
        flash('Cart empty')
        return redirect(url_for('user.cart'))

    total = 0
    order = Order(user_id=user.id, status='Pending')
    DB.session.add(order)
    DB.session.flush()  # Get order.id before committing

    for ci in items:
        if ci.product.quantity < ci.qty:
            flash(f'Not enough stock for {ci.product.name}')
            DB.session.rollback()
            return redirect(url_for('user.cart'))

        ci.product.quantity -= ci.qty
        oi = OrderItem(order_id=order.id, product_id=ci.product.id, qty=ci.qty, price=ci.product.price)
        total += ci.qty * ci.product.price
        DB.session.add(oi)
        DB.session.delete(ci)

    order.total = total
    DB.session.commit()
    flash('Order placed')
    return redirect(url_for('user.products'))
