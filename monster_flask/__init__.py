from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from monster_flask.config import Config

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
# db = SQLAlchemy(app)

db = SQLAlchemy()


def create_app(cfg=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from monster_flask.game import game
    app.register_blueprint(game)

    return app
