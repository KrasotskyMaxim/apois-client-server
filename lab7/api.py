from bottle import (
    debug,
    route, 
    request,
    run,
)
import logging
import settings


@route("/api/")
def index():
    logging.info("go /api/ by GET request")
    return settings.API_URLS 


@route("/api/models/")
def models():
    logging.info("go /api/models by GET request")
    return settings.MODELS 


@route("/api/<model>/")
def get(model, db):
    logging.info("go /%s/get/ by GET request", model)
    data_list = db.execute(f"SELECT * FROM {settings.MODELS[model]};").fetchall()
    
    response_data = {}
    for row in data_list:
        row = dict(row)
        obj_id = row.pop("id")
        response_data[obj_id] = row
    return response_data


@route("/api/<model>/create/", method="POST")
def create(model, db):
    logging.info("read data by POST request for path /%s/create/", model)
    data = request.json

    match model:
        case "users":
            db.execute(
                '''
                INSERT INTO Users (name, email, password)
                VALUES (?, ?, ?);
                ''', (data.get("name"), data.get("email"), data.get("password"))
            )
        case "products":
            db.execute(
                '''
                INSERT INTO Products (name, price, category_name)
                VALUES (?, ?, ?);
                ''', (data.get("name"), data.get("price"), data.get("category_name"))
            )
        case "orders":
            db.execute(
                '''
                INSERT INTO Orders (user_id, product_name, quantity)
                VALUES (?, ?, ?);
                ''', (data.get("user_id"), data.get("product_name"), data.get("quantity"))
            )
        case "categorys":
            db.execute(
                '''
                INSERT INTO Categorys (name)
                VALUES (?);
                ''', (data.get("name"),)
            )
    
    db.commit()
    return {"message": f"{model} successful created!"}


@route("/api/<model>/delete/", method="POST")
def delete(model, db):
    logging.info("read data by POST request for path /%s/delete/", model)
    data = request.json

    db.execute(f"DELETE FROM {settings.MODELS[model]} WHERE id=?;", (data.get("id"),))
    
    db.commit()  
    return {"message": f"{model} successful deleted!"}


@route("/api/<model>/edit/", method="POST")
def edit(model, db):
    logging.info("read data by POST request for path /%s/edit/", model)
    data = request.json
    
    match model:
        case "users":
            db.execute(
                '''
                UPDATE Users
                SET name = ?, email = ?, password = ?
                WHERE id = ?;
                ''', (
                    data.get("new_name"), 
                    data.get("new_email"), 
                    data.get("new_password"), 
                    data.get("id")
                )
            )
        case "products":
            db.execute(
                '''
                UPDATE Products
                SET name = ?, price = ?, category_name = ?
                WHERE id = ?;
                ''', (
                    data.get("new_name"), 
                    data.get("new_price"), 
                    data.get("new_category_name"),
                    data.get("id")    
                )
            )
        case "orders":
            db.execute(
                '''
                UPDATE Orders
                SET user_id = ?, product_name = ?, quantity = ?
                WHERE id = ?;
                ''', (
                    data.get("new_user_id"), 
                    data.get("new_product_name"), 
                    data.get("new_quantity"),
                    data.get("id")    
                )
            )
        case "categorys":
            db.execute(
                '''
                UPDATE Categorys
                SET name = ?
                WHERE id = ?;
                ''', (
                    data.get("new_name"),
                    data.get("id")    
                )
            )
    
    db.commit()  
    return {"message": f"{model} successful edited!"}


if __name__ == "__main__":
    debug(settings.DEBUG)
    run(host=settings.API_HOST, port=settings.API_PORT, reloader=True)
