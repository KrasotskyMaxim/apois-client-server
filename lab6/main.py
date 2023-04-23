from bottle import (
    route, 
    template, 
    request,
    run,
    abort,
)
# from bottle_sqlite import SQLitePlugin
# install(SQLitePlugin(dbfile='/tmp/test.db'))


@route("/")
def index():
    name = request.query.get("name", "World")
    return template("index.tpl", name=name)


@route("<model>/list", method="GET")
def list(model):
    match(model):
        case "User":
            pass
        case "Product":
            pass
        case "Order":
            pass
        case "Category":
            pass
        case _:
            abort(404, "Not Found")


@route("<model>/create", method="POST")
def create(model):
    match(model):
        case "User":
            pass
        case "Product":
            pass
        case "Order":
            pass
        case "Category":
            pass
        case _:
            abort(404, "Not Found")


@route("<model>/<id>/edit", method="PUT")
def edit(model, id):
    match(model):
        case "User":
            pass
        case "Product":
            pass
        case "Order":
            pass
        case "Category":
            pass
        case _:
            abort(404, "Not Found")
        

@route("<model>/<id>/delete", method="DELETE")
def delete(model, id):
    match(model):
        case "User":
            pass
        case "Product":
            pass
        case "Order":
            pass
        case "Category":
            pass
        case _:
            abort(404, "Not Found")


if __name__ == "__main__":
    run(host="localhost", port=8000, debug=True, reloader=True)