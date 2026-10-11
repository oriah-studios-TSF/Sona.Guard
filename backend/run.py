# Import the application factory function from the app package.
# An application factory creates and configures our Flask app instance on demand.
from app import create_app

# Instantiate the Flask application using our factory.
app = create_app()

# This conditional block ensures the development server only starts when this script
# is executed directly (e.g. `python run.py`), and not when imported as a module by tests
# or production WSGI servers (such as Gunicorn or uWSGI).
if __name__ == '__main__':
    # Start the local development web server.
    # Note: `debug=True` enables automatic code reloading and an interactive browser debugger.
    # It is intended only for local development and should be turned off in production,
    # as the interactive debugger allows arbitrary code execution if exposed.
    app.run(debug=True)