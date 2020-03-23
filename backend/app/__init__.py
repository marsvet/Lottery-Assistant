from flask import Flask
from flask_apscheduler import APScheduler
from config import Config
from app.models import Database
from app.crawler import Crawler

scheduler = APScheduler()
config = Config()
db = Database()
crawler = Crawler()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    scheduler.init_app(app)
    scheduler.start()

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
