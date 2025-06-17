from flask import Flask
import sys
import os

# If 'app' is the package, imports should be 'from app.api.routes...'
# This assumes that the Python interpreter is run from the directory containing 'app'
# or 'app' is in PYTHONPATH. For 'python app/main.py', current dir is 'app'.
# For Flask CLI 'flask run', it usually auto-detects 'app' or 'wsgi.py'.

def create_app():
    # __name__ resolves to 'app.main' if main.py is in 'app' package.
    # Explicitly set template_folder and static_folder relative to the app's root path.
    # app.root_path is the 'app' directory (e.g. /app/app) if main.py is app/main.py.
    # Templates/static are in /app/templates and /app/static, so use ../
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Ensure instance folder exists (if needed for SQLite etc., not currently used)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # Already exists or permission issue

    # Import and register API blueprint
    # Assuming api.routes is app/api/routes.py
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Import and register UI blueprint
    # Assuming ui_routes is app/ui_routes.py
    from app.ui_routes import ui_bp
    app.register_blueprint(ui_bp, url_prefix='/') # UI will be at the root

    @app.route('/status')
    def status():
        return "Base40 Cryptographic Suite Backend (and UI) is running!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
