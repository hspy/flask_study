from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from sqlalchemy import MetaData

import config

#set for db
#since they will used in other modules(like blueprint)
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention)) #메타데이터 클래스를 이용하여 규칙을 정의해야 함
migrate = Migrate()


def create_app():
    app = Flask(__name__) #flask app
    app.config.from_object(config) #db config

    # ORM
    db.init_app(app) #db object orm init(SQL)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True) #render as batch를 true를 해줘야 제약조건의 변경을 지원하지 않음
    else:
        migrate.init_app(app, db)
    from . import models

    # blueprint
    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp) #views
    app.register_blueprint(question_views.bp) #question view
    app.register_blueprint(answer_views.bp) #answer view
    app.register_blueprint(auth_views.bp) # login
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    from .filter import format_datetime #템플릿 필터
    app.jinja_env.filters['datetime'] = format_datetime 
 
    Markdown(app, extensions=['nl2br', 'fenced_code']) # 마크다운 기능
    return app