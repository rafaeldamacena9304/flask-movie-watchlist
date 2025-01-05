from flask import Flask
from pymongo import MongoClient

client = MongoClient("MONGODB_URI")
db = client["main"]

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'YOUR_SECRET_KEY'

    from app.routes import main
    app.register_blueprint(main)

    return app