from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from routes import register_blueprints
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'tem.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('TEM_SECRET', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)
register_blueprints(app, db)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    from models import init_db
    init_db(app, db)
    app.run(debug=True)
