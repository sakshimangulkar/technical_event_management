from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Placeholder for lazy assignment
DB = None  

def init_db(app, db):
    """Initialize database and create tables."""
    global DB
    DB = db
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")


class User:
    id = None  # for IDE hints


# Use DB instead of db
class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120), nullable=False)
    email = DB.Column(DB.String(120), unique=True, nullable=False)
    password_hash = DB.Column(DB.String(256), nullable=False)
    role = DB.Column(DB.String(20), default='user')  # user, vendor, admin

    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)
