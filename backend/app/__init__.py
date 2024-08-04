from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config') 
    CORS(app)
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
