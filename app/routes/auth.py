from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id: str, username: str, password: str):
        self.id = id
        self.username = username
        self.password = password

users = {
    "1": User("1", "luke", "self1234")
}

# Find user in database
def find_user_by_username(username):
    for user in users.values():
        if user.username == username:
            return user
    return None

# Find user by id
def find_user_by_id(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
        return None

# Authenticate user
def authenticate(username, password):
    user = find_user_by_username(username)

    if not user:
        return None
    
    if password == user.password:
        return user
    
    return None