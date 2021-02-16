from monster_flask.users import models
from monster_flask.utils import ModelController


class UserController(ModelController):
    @staticmethod
    def get_user_id(username):
        user = models.User.query.filter_by(username=username).first()

        if user:
            return user.id

    @staticmethod
    def get_user_by_id(user_id):
        return models.User.query.get(user_id)

    @staticmethod
    def check_login(username, password):
        user = models.User.query.filter_by(username=username).first()

        if not user:
            return {"error": f"No user found with username: '{username}'"}

        if user.check_password(password):
            return UserController.get_user_data(user)

        else:
            return {"error": "Incorrect password"}

    def add_user(self, username, password):
        user = models.User(username=username)
        user.set_password(password)
        self.add(user)

        return user

    # API methods

    def get_all_users(self):
        return [self.get_user_data(u) for u in models.User.query.all()]

    @staticmethod
    def get_user_data(user):
        return {
            "username": user.username,
            "id": user.id
        }
