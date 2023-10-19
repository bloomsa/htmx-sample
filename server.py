import sys
from pathlib import Path

### BOILERPLATE TO MINIMIZE DEMO SETUP FOR YOU, IGNORE ###
CUR_DIR = Path(__file__).resolve().parent
sys.path.append(str(CUR_DIR.parent))

import todo
from bottle import TEMPLATE_PATH, debug, redirect, request, route, run, template

TEMPLATE_PATH.append(str(CUR_DIR))
### END BOILER PLATE ###


@route("/")
def index():
    """List all the tasks, count them, then render the index page template"""

    tasks = todo.list_todos()
    counts = todo.count_todos()
    return template("index", tasks=tasks, counts=counts)


@route("/add", method="POST")
def add():
    """Add one task, and redirect to the index"""

    title = request.forms.get("title")
    if title:
        todo.add_todo(title)
    redirect("/")


@route("/set_task_status", method="POST")
def set_task_status():
    """Set the status of all the task, then redirect to the index"""

    all_tasks = todo.list_todos()
    done_task_ids = set(int(task_id) for task_id in request.forms.getall("task"))
    for task in all_tasks:
        new_status = task["id"] in done_task_ids
        todo.set_task_status(task["id"], new_status)
    redirect("/")


@route("/delete/<task_id:int>", method="GET")
def delete(task_id):
    """Delete one task and redirect to the template"""

    todo.delete_todo(task_id)
    redirect("/")

# Start the server
if __name__ == "__main__":
    run(host="localhost", port=8080)