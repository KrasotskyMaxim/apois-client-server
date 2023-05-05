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

DEBUG = True if os.getenv("DEBUG") else False


bottle.TEMPLATE_PATH += [
    "./views/users/",
    "./views/orders/",
    "./views/categorys/",
    "./views/products/",
]


MODELS = {
    "users": "Users",
    "products": "Products", 
    "categorys": "Categorys", 
    "orders": "Orders",
}
