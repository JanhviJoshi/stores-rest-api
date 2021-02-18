from resources.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):  # payload is the JWT
    user_id = payload['identity']  # extracting id from JWT
    return UserModel.find_by_id(user_id)
