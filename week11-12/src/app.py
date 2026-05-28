from flask import Flask, jsonify

from docs import swagger_html
from routes.activity_routes import activity_bp
from routes.integration_routes import integration_bp
from routes.project_routes import project_bp
from routes.task_routes import task_bp
from services.dispatcher import EventDispatcher
from services.integration_service import IntegrationService


def create_app():

    app = Flask(__name__)

    dispatcher = EventDispatcher()

    integration_service = IntegrationService()

    dispatcher.subscribe(
        "task.created",
        integration_service.send_event
    )

    dispatcher.subscribe(
        "task.completed",
        integration_service.send_event
    )

    app.dispatcher = dispatcher

    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(integration_bp)

    @app.route("/", methods=["GET"])
    def home():

        return jsonify({
            "service": "TaskFlow API",
            "patterns": [
                "CRUD",
                "Query",
                "HATEOAS",
                "Event-driven",
                "Webhook"
            ],
            "_links": {
                "projects": "/api/projects",
                "tasks": "/api/tasks",
                "events": "/api/events",
                "docs": "/docs"
            }
        })

    @app.route("/docs", methods=["GET"])
    def docs():

        return swagger_html()

    @app.route("/openapi.json", methods=["GET"])
    def openapi():

        return jsonify({
            "openapi": "3.0.3",
            "info": {
                "title": "TaskFlow API",
                "version": "1.0.0"
            }
        })

    return app