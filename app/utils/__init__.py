from app.routes import main  # Adjust if necessary based on your project structure
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Initialize extensions here, like db.init_app(app)
    
    # Register the main blueprint
    app.register_blueprint(main.bp)
    
    return app
