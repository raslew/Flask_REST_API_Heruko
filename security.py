
from models.user import UserModel

def authenticate(username, password):
    #None sätts som ett defaultvärde och används ifall "username" inte finns.
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    #Payload är token från flask_JWT
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
