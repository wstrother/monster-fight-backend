from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from monster_flask import db
from monster_flask.utils import password_strength


class User(db.Model):
    id_no = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    monsters = db.relationship('Monster', backref="owner", lazy=True,
                               foreign_keys="Monster.owner_id")

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise AssertionError('No username provided')

        if User.query.filter(User.username == username).first():
            raise AssertionError('Username is already in use')

        if len(username) < 5 or len(username) > 30:
            raise AssertionError('Username must be between 5 and 30 characters')

        return username

    def set_password(self, password):
        if not password:
            raise AssertionError('Password not provided')

        if not password_strength(password):
            raise AssertionError(
                'Password must contain at least 1 capital letter, lowercase letter, numeral and other symbol'
            )

        if len(password) < 8 or len(password) > 50:
            raise AssertionError('Password must be between 8 and 50 characters')

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)