from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # initialized later in app.py

# --------------------------
# USER MODEL
# --------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # can be admin/vendor/user

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)


# --------------------------
# PRODUCT MODEL
# --------------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)

    vendor = db.relationship('User', backref='products')


# --------------------------
# CART MODEL
# --------------------------
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product')


# --------------------------
# ORDER MODEL
# --------------------------
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')

    user = db.relationship('User', backref='orders')


# --------------------------
# ORDER ITEM MODEL
# --------------------------
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    order = db.relationship('Order', backref='order_items')
    product = db.relationship('Product')


# --------------------------
# INIT DB FUNCTION
# --------------------------
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
