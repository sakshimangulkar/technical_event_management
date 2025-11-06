def create_default_admin(db):
    from models import User

    if not User.query.filter_by(role='admin').first():
        admin = User(name='Admin', email='admin@tem.local', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
