from flask import Flask
from models import db
from routes import register_blueprints

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with Flask app
db.init_app(app)

register_blueprints(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
