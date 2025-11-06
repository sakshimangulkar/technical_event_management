# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tem.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create SQLAlchemy instance
db = SQLAlchemy(app)

# Now import models after DB exists
from models import User, Product, CartItem, Order, OrderItem
from routes import register_blueprints

# Register blueprints
register_blueprints(app, db)

if __name__ == '__main__':
    # Create tables if not exist
    db.create_all()
    app.run(debug=True)
