import math
import uuid
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from database import PROJECTS, TASKS
from helpers.links import project_links

project_bp = Blueprint("project_bp", __name__)


@project_bp.route("/api/projects", methods=["POST"])
def create_project():

    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    owner = (data.get("owner") or "").strip()

    if not name or not owner:
        return jsonify({
            "error": "Missing fields"
        }), 400

    project = {
        "id": str(uuid.uuid4()),
        "name": name,
        "owner": owner,
        "status": "active",
        "created_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    project["_links"] = project_links(
        project["id"]
    )

    PROJECTS.append(project)

    return jsonify(project), 201


@project_bp.route("/api/projects", methods=["GET"])
def list_projects():

    items = PROJECTS.copy()

    search = request.args.get("search")
    owner = request.args.get("owner")

    page = int(
        request.args.get("page", 1)
    )

    limit = int(
        request.args.get("limit", 5)
    )

    if search:
        items = [
            item for item in items
            if search.lower() in item["name"].lower()
        ]

    if owner:
        items = [
            item for item in items
            if item["owner"].lower() == owner.lower()
        ]

    total_items = len(items)

    start = (page - 1) * limit
    end = start + limit

    paginated = items[start:end]

    return jsonify({
        "data": paginated,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": math.ceil(
                total_items / limit
            ) if limit else 1
        }
    })


@project_bp.route("/api/projects/<project_id>", methods=["GET"])
def get_project(project_id):

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

    return jsonify(project)


@project_bp.route("/api/projects/<project_id>", methods=["DELETE"])
def delete_project(project_id):

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

    PROJECTS.remove(project)

    return jsonify({
        "message": "Deleted"
    })


@project_bp.route(
    "/api/projects/<project_id>/tasks",
    methods=["GET"]
)
def project_tasks(project_id):

    tasks = [
        task for task in TASKS
        if task["project_id"] == project_id
    ]

    return jsonify({
        "count": len(tasks),
        "data": tasks
    })