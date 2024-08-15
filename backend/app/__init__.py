from flask import Flask, jsonify
from .routes import bp as routes_bp 

def create_app():
    app = Flask(__name__)

    # Enregistrement du Blueprint
    app.register_blueprint(routes_bp)
    
    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.route('/get_exchange_rates')
    def get_exchange_rates():
        return jsonify({"rates": "data"})

    # autres routes et configurations...
    
    return app
