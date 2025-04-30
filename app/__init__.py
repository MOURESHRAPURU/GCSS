# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from config import Config

# db = SQLAlchemy()
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     db.init_app(app)
#     login_manager.init_app(app)

#     from app.routes import auth, admin, counselor
#     app.register_blueprint(auth.bp)
#     app.register_blueprint(admin.bp)
#     app.register_blueprint(counselor.bp)

#     return app

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect to the login view

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class

    # Initialize the database and login manager
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()  # Create database tables

    # Define the user loader function
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Import User model to avoid circular imports
        return User.query.get(int(user_id))

    # Register blueprints with URL prefixes
    from app.routes import auth, admin, counselor
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(counselor.bp, url_prefix='/counselor')

    # Define a root route that redirects to the login page
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

