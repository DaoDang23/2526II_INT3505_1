def project_links(project_id):
    return {
        "self": {
            "href": f"/api/projects/{project_id}",
            "method": "GET"
        },
        "tasks": {
            "href": f"/api/projects/{project_id}/tasks",
            "method": "GET"
        },
        "delete": {
            "href": f"/api/projects/{project_id}",
            "method": "DELETE"
        }
    }


def task_links(task_id, project_id):
    return {
        "self": {
            "href": f"/api/tasks/{task_id}",
            "method": "GET"
        },
        "complete": {
            "href": f"/api/tasks/{task_id}/complete",
            "method": "PATCH"
        },
        "project": {
            "href": f"/api/projects/{project_id}",
            "method": "GET"
        }
    }