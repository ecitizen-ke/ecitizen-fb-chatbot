# from flask import Flask
# from backend.config import config

# def create_app(config_name):
#     app = Flask(__name__)
#     app.config.from_object(config[config_name])
#     register_blueprints(app)
#     initialize_extensions(app)
#     return app

# # ---------------------------------------------
# # helper functions
# # ---------------------------------------------
# def initialize_extensions(app):
#     from backend.extensions import db, migrate, bcrypt

#     db.init_app(app)
#     with app.app_context():
#         db.create_all()
#     migrate.init_app(app, db)
#     bcrypt.init_app(app)

# def register_blueprints(app):
#     from .api.auth.views import auth_blueprint
#     from .api.facebook_api.views import facebook_api_bp
#     from .api.dashboard.views import dashboard_bp

#     # Auth blueprint
#     app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")
#     # Facebook webhook blueprint
#     app.register_blueprint(facebook_api_bp, url_prefix="/api/v1/facebook")
#     # Dashboard blueprint
#     app.register_blueprint(dashboard_bp, url_prefix="/api/v1/dashboard")

from flask import Flask
from backend.config import config
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Load VERIFY_TOKEN and FB_PAGE_ACCESS_TOKEN from environment
    app.config['VERIFY_TOKEN'] = os.getenv('VERIFY_TOKEN')
    app.config['FB_PAGE_ACCESS_TOKEN'] = os.getenv('FB_PAGE_ACCESS_TOKEN')

    register_blueprints(app)
    initialize_extensions(app)
    return app

# ---------------------------------------------
# helper functions
# ---------------------------------------------
def initialize_extensions(app):
    from backend.extensions import db, migrate, bcrypt

    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate.init_app(app, db)
    bcrypt.init_app(app)

def register_blueprints(app):
    from .api.auth.views import auth_blueprint
    from .api.facebook_api.views import facebook_api_bp
    from .api.dashboard.views import dashboard_bp

    # Auth blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")
    # Facebook webhook blueprint
    app.register_blueprint(facebook_api_bp, url_prefix="/api/v1/facebook")
    # Dashboard blueprint
    app.register_blueprint(dashboard_bp, url_prefix="/api/v1/dashboard")

