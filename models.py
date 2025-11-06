from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Define models using a DB placeholder; app will assign DB to the SQLAlchemy instance
DB = None


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120), nullable=False)
    email = DB.Column(DB.String(120), unique=True, nullable=False)
    password_hash = DB.Column(DB.String(256), nullable=False)
    role = DB.Column(DB.String(20), default='user')  # user, vendor, admin

    products = DB.relationship('Product', backref='vendor', lazy=True)
    cart_items = DB.relationship('CartItem', backref='user', lazy=True)
    orders = DB.relationship('Order', backref='user', lazy=True)

    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)


class Product(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    vendor_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=True)
    name = DB.Column(DB.String(200), nullable=False)
    description = DB.Column(DB.String(500), default='')
    price = DB.Column(DB.Float, nullable=False)
    quantity = DB.Column(DB.Integer, default=0)
    created_at = DB.Column(DB.DateTime, default=datetime.utcnow)


class CartItem(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'))
    product_id = DB.Column(DB.Integer, DB.ForeignKey('product.id'))
    qty = DB.Column(DB.Integer, default=1)

    product = DB.relationship('Product')


class Order(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'))
    status = DB.Column(DB.String(50), default='Pending')
    total = DB.Column(DB.Float, default=0.0)
    created_at = DB.Column(DB.DateTime, default=datetime.utcnow)

    items = DB.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    order_id = DB.Column(DB.Integer, DB.ForeignKey('order.id'))
    product_id = DB.Column(DB.Integer, DB.ForeignKey('product.id'))
    qty = DB.Column(DB.Integer, default=1)
    price = DB.Column(DB.Float, default=0.0)

    product = DB.relationship('Product')
