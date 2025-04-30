### <---------- Imports ---------->
# Import Flask and configuration settings
from flask import Flask, session
from config import Config 

# Importing blueprints for routing
from chat.route.chatRoute import chat_bp
from dashboard.routes.dashRoutes import dash_bp

# Importing database initialization function
from database.database.database import initializeDb

# Importing CORS for cross-origin requests handling
from flask_cors import CORS

### <---------- App Setup ---------->
# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app, origins="*", supports_credentials=True)  # Allow all domains (for testing)

# # Simulated in-memory session store
# session_store = {}

# Set the secret key for sessions
app.secret_key = 'your_secret_key'

# # <---------- Session Configuration ---------->
# # Configure session type (could use 'redis', 'sqlalchemy', etc.)
# app.config['SESSION_TYPE'] = 'filesystem'

# # Make session non-permanent (session data won't persist after closing the browser)
# app.config['SESSION_PERMANENT'] = False

# # Use a signer for session cookies
# app.config['SESSION_USE_SIGNER'] = True

# # Optional (for iframe + https cases)
# app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Ensures cookies work with cross-site requests
# app.config['SESSION_COOKIE_SECURE'] = False  # Cookies won't be sent over HTTPS in this case

# <---------- Configuration Loading ---------->
# Load configuration settings from config.py
app.config.from_object(Config)

# <---------- Database Initialization ---------->
# Initialize the database connection
initializeDb(app)

# <---------- Blueprint Registration ---------->
# Register the 'chat' and 'dashboard' blueprints
app.register_blueprint(chat_bp, url_prefix='/')
app.register_blueprint(dash_bp, url_prefix='/dashboard')

### <---------- After Request Handling ---------->
# This function runs after each request to modify the response headers
# @app.after_request
# def after_request(response):
#     response.headers['X-Frame-Options'] = 'ALLOWALL'  # Allow iframe embedding
#     response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins
#     return response

### <---------- Main Entry Point ---------->
# Start the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)

# # Uncomment for debugging with Flask’s built-in server
# if __name__ == "__main__":
#     app.run(debug=True)
