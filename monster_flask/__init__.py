from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from monster_flask.config import Config

db = SQLAlchemy()


def create_app(cfg=Config):
    app = Flask(__name__)
    app.config.from_object(cfg)
    db.init_app(app)

    from monster_flask.game import game
    app.register_blueprint(game)

    from monster_flask.users import users
    app.register_blueprint(users)

    return app
