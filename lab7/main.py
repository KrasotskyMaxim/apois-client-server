from bottle import (
    debug,
    route, 
    template, 
    request,
    run,
    abort,
    redirect,
)
import requests
import logging
import settings


@route("/")
def index():
    logging.info("go / by GET request")
    url = settings.API_REQUESTS_URL+"/models/"
    response = requests.get(url)

    if (code := response.status_code) != 200:
        logging.warning("Error response to %s with status %s", url, code)
        abort(500, "API server error")
        
    models = response.json()
    return template("index.tpl", models=models)


@route("/<model>/get/")
def get(model):
    logging.info("go /%s/get/ by GET request", model)
    if (model := model.lower()) not in settings.MODELS:
        logging.warning("path /%s/get/ not found", model)    
        abort(404, "Not Found")
    
    url = f"{settings.API_REQUESTS_URL}/{model}/"
    response = requests.get(url)
    
    if (code := response.status_code) != 200:
        logging.warning("Error response to %s with status %s", url, code)
        abort(500, "API server error")
    
    data_list = response.json()
    return template("get.tpl", data_list=data_list, model=model)        


@route("/<model>/create/")
@route("/<model>/create/", method="POST")
def create(model):
    if (model := model.lower()) not in settings.MODELS:
        logging.warning("path /%s/create/ not found", model)    
        abort(404, "Not Found")

    if request.method == "GET":
        logging.info("return create form by GET request for path /%s/create/", model)
        return template(f"create_form_{settings.MODELS[model]}.tpl")   
    
    url = f"{settings.API_REQUESTS_URL}/{model}/create/"
    data = dict(request.forms)
    response = requests.post(url, json=data)
    
    if (code := response.status_code) != 200:
        logging.warning("Error response to %s with status %s", url, code)
        abort(500, "API server error")
    
    logging.info("redirect to /%s/get/ path after creating object", model)
    redirect(f"/{model}/get/")

        
@route("/<model>/delete/")
@route("/<model>/delete/", method="POST")
def delete(model):
    if (model := model.lower()) not in settings.MODELS:
        logging.warning("path /%s/delete/ not found", model)    
        abort(404, "Not Found")

    if request.method == "GET":
        logging.info("return delete form by GET request for path /%s/delete/", model)
        return template(f"delete.tpl", model=model)   
    
    url = f"{settings.API_REQUESTS_URL}/{model}/delete/"
    data = dict(request.forms)
    response = requests.delete(url, json=data)
    
    if (code := response.status_code) != 200:
        logging.warning("Error response to %s with status %s", url, code)
        abort(500, "API server error")
    
    logging.info("redirect to /%s/get/ path after deleting object", model)
    redirect(f"/{model}/get/")
        

@route("/<model>/edit/")    
@route("/<model>/edit/", method="POST")
def edit(model):
    if (model := model.lower()) not in settings.MODELS:
        logging.warning("path /%s/edit/ not found", model)    
        abort(404, "Not Found")

    if request.method == "GET":
        logging.info("return edit form by GET request for path /%s/edit/", model)
        return template(f"edit_form_{settings.MODELS[model]}.tpl")   

    url = f"{settings.API_REQUESTS_URL}/{model}/edit/"
    data = dict(request.forms)
    response = requests.put(url, json=data)
    
    if (code := response.status_code) != 200:
        logging.warning("Error response to %s with status %s", url, code)
        abort(500, "API server error")

    logging.info("redirect to /%s/get/ path after editing object", model)
    redirect(f"/{model}/get/")
    

if __name__ == "__main__":
    debug(settings.DEBUG)
    run(host=settings.HOST, port=settings.PORT, reloader=True)
