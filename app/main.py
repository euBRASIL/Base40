from flask import Flask
import sys
import os

# Ensure the 'app' directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_app():
    app = Flask(__name__)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Import and register blueprints
    from app.api.routes import api_bp  # Corrected import path
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def hello():
        return "Base40 Cryptographic Suite Backend is running!"

    return app

if __name__ == '__main__':
    app = create_app()
    # Note: For development, app.run() is fine.
    # For production, use a WSGI server like Gunicorn or Waitress.
    app.run(debug=True, host='0.0.0.0', port=5000)
