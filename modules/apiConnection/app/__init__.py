from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect Connection API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    @app.before_request
    def before_request():
        # Set up a Kafka producer
        # Setting Kafka to g enables us to use this
        # in other parts of our application        
        config = config_by_name[env or "test"]
        PERSONS_ENDPOINT = config.PERSONS_ENDPOINT
        g.PERSONS_ENDPOINT = PERSONS_ENDPOINT

        # g.kafka_producer = "producer hello!"

    return app
