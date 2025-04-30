from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Check if an admin already exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('your-password')  # Replace with a secure password
        admin.access_level = '1'
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists.")
