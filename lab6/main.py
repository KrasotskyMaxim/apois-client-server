from bottle import (
    debug,
    route, 
    template, 
    request,
    run,
    abort,
    redirect,
)
import logging
import settings


@route("/")
def index():
    logging.info("go / by GET request")
    return template("index.tpl")


@route("/<model>/get/")
def get(model, db):
    logging.info("go /%s/get/ by GET request", model)
    if (model := model.lower()) not in settings.MODELS:
        logging.warning("path /%s/get/ not found", model)    
        abort(404, "Not Found")
    
    data_list = db.execute(f"SELECT * FROM {settings.MODELS[model]};").fetchall()
    return template("get.tpl", data_list=data_list, model=model)        


@route("/<model>/create/")
@route("/<model>/create/", method="POST")
def create(model, db):
    if (model := model.lower()) not in settings.MODELS:
        logging.warning("path /%s/create/ not found", model)    
        abort(404, "Not Found")

    if request.method == "GET":
        logging.info("return create form by GET request for path /%s/create/", model)
        return template(f"create_form_{settings.MODELS[model]}.tpl")   
    
    logging.info("read form data by POST request for path /%s/create/", model)
    match model:
        case "users":
            db.execute(
                '''
                INSERT INTO Users (name, email, password)
                VALUES (?, ?, ?);
                ''', (request.forms.name, request.forms.email, request.forms.password)
            )
        case "products":
            db.execute(
                '''
                INSERT INTO Products (name, price, category_name)
                VALUES (?, ?, ?);
                ''', (request.forms.name, request.forms.price, request.forms.category_name)
            )
        case "orders":
            db.execute(
                '''
                INSERT INTO Orders (user_id, product_name, quantity)
                VALUES (?, ?, ?);
                ''', (request.forms.user_id, request.forms.product_name, request.forms.quantity)
            )
        case "categorys":
            db.execute(
                '''
                INSERT INTO Categorys (name)
                VALUES (?);
                ''', (request.forms.name,)
            )
    
    db.commit()  
    logging.info("redirect to /%s/get/ path after creating object", model)
    redirect(f"/{model}/get/")

        
@route("/<model>/delete/")
@route("/<model>/delete/", method="POST")
def delete(model, db):
    if (model := model.lower()) not in settings.MODELS:
        logging.warning("path /%s/delete/ not found", model)    
        abort(404, "Not Found")

    if request.method == "GET":
        logging.info("return delete form by GET request for path /%s/delete/", model)
        return template(f"delete.tpl", model=model)   
    
    logging.info("read form data by POST request for path /%s/delete/", model)
    db.execute(f"DELETE FROM {settings.MODELS[model]} WHERE id={request.forms.id};")
    db.commit()  
    logging.info("redirect to /%s/get/ path after deleting object", model)
    redirect(f"/{model}/get/")
        

@route("/<model>/edit/")    
@route("/<model>/edit/", method="POST")
def edit(model, db):
    if (model := model.lower()) not in settings.MODELS:
        logging.warning("path /%s/edit/ not found", model)    
        abort(404, "Not Found")

    if request.method == "GET":
        logging.info("return edit form by GET request for path /%s/edit/", model)
        return template(f"edit_form_{settings.MODELS[model]}.tpl")   

    logging.info("read form data by POST request for path /%s/edit/", model)
    match model:
        case "users":
            db.execute(
                '''
                UPDATE Users
                SET name = ?, email = ?, password = ?
                WHERE id = ?;
                ''', (
                    request.forms.new_name, 
                    request.forms.new_email, 
                    request.forms.new_password, 
                    request.forms.id
                )
            )
        case "products":
            db.execute(
                '''
                UPDATE Products
                SET name = ?, price = ?, category_name = ?
                WHERE id = ?;
                ''', (
                    request.forms.new_name, 
                    request.forms.new_price, 
                    request.forms.new_category_name,
                    request.forms.id    
                )
            )
        case "orders":
            db.execute(
                '''
                UPDATE Orders
                SET user_id = ?, product_name = ?, quantity = ?
                WHERE id = ?;
                ''', (
                    request.forms.new_user_id, 
                    request.forms.new_product_name, 
                    request.forms.new_quantity,
                    request.forms.id    
                )
            )
        case "categorys":
            db.execute(
                '''
                UPDATE Categorys
                SET name = ?
                WHERE id = ?;
                ''', (
                    request.forms.new_name,
                    request.forms.id    
                )
            )
    
    db.commit()  
    logging.info("redirect to /%s/get/ path after editing object", model)
    redirect(f"/{model}/get/")
    

if __name__ == "__main__":
    debug(settings.DEBUG)
    run(host=settings.HOST, port=settings.PORT, reloader=True)
