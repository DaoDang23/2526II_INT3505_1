import uuid
from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify, request

from database import PROJECTS, TASKS
from helpers.links import task_links

task_bp = Blueprint("task_bp", __name__)


@task_bp.route("/api/tasks", methods=["POST"])
def create_task():

    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()

    project_id = data.get("project_id")

    priority = (
        data.get("priority") or "medium"
    )

    if not title or not project_id:
        return jsonify({
            "error": "Missing fields"
        }), 400

    project = next(
        (
            item for item in PROJECTS
            if item["id"] == project_id
        ),
        None
    )

    if not project:
        return jsonify({
            "error": "Project not found"
        }), 404

    task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "project_id": project_id,
        "priority": priority,
        "status": "todo",
        "created_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    task["_links"] = task_links(
        task["id"],
        project_id
    )

    TASKS.append(task)

    current_app.dispatcher.publish(
        "task.created",
        task
    )

    return jsonify(task), 201


@task_bp.route("/api/tasks", methods=["GET"])
def list_tasks():

    items = TASKS.copy()

    status = request.args.get("status")
    priority = request.args.get("priority")
    search = request.args.get("search")

    if status:
        items = [
            item for item in items
            if item["status"] == status
        ]

    if priority:
        items = [
            item for item in items
            if item["priority"] == priority
        ]

    if search:
        items = [
            item for item in items
            if search.lower() in item["title"].lower()
        ]

    return jsonify({
        "count": len(items),
        "data": items
    })


@task_bp.route("/api/tasks/<task_id>", methods=["GET"])
def get_task(task_id):

    task = next(
        (
            item for item in TASKS
            if item["id"] == task_id
        ),
        None
    )

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify(task)


@task_bp.route(
    "/api/tasks/<task_id>/complete",
    methods=["PATCH"]
)
def complete_task(task_id):

    task = next(
        (
            item for item in TASKS
            if item["id"] == task_id
        ),
        None
    )

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    task["status"] = "done"

    task["completed_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    current_app.dispatcher.publish(
        "task.completed",
        task
    )

    return jsonify(task)