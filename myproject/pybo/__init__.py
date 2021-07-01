from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

#set for db
#since they will used in other modules(like blueprint)
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__) #flask app
    app.config.from_object(config) #db config

    # ORM
    db.init_app(app) #db object orm init(SQL)
    migrate.init_app(app, db) # init app with db
    from . import models

    # blueprint
    from .views import main_views, question_views
    app.register_blueprint(main_views.bp) #views
    app.register_blueprint(question_views.bp) #question view

    return app