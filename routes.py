from auth_routes import auth_bp
from vendor_routes import vendor_bp
from user_routes import user_bp
from admin_routes import admin_bp



def register_blueprints(app, db):
    # lazy import models and attach db
    import models
    models.DB = db

    app.register_blueprint(auth_bp)
    app.register_blueprint(vendor_bp, url_prefix='/vendor')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
