import bottle
import logging

from bottle_sqlite import SQLitePlugin
from bottle import install

from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
install(SQLitePlugin(dbfile=os.getenv("DB_PATH")))


HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")
API_URL = os.getenv("API_URL")
API_REQUESTS_URL= f"http://{API_HOST}:{API_PORT}{API_URL}"

TEMPLATE_DIR = os.getenv("TEMPLATE_DIR")

DEBUG = True if os.getenv("DEBUG") else False


bottle.TEMPLATE_PATH += [
    TEMPLATE_DIR + path for
    path in [
        "/users/",
        "/orders/",
        "/categorys/",
        "/products/",
    ]
]


MODELS = {
    "users": "Users",
    "products": "Products", 
    "categorys": "Categorys", 
    "orders": "Orders",
}

API_URLS = {
    "info": f"GET {API_URL}/",
    "models": f"GET {API_URL}/models/",
    "model_list": f"GET {API_URL}/<model>/",
    "obj_info": f"GET {API_URL}/<model>/<obj_id>/",
    "create_obj": f"POST {API_URL}/<model>/create/",
    "edit_obj": f"PUT {API_URL}/<model>/<obj_id>/",
    "delete_obj": f"DELETE {API_URL}/<model>/<obj_id>/"
}