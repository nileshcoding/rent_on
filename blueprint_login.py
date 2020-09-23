from flask import Flask
from flask import Blueprint
from flask import request
from functions import *
import time
import json
import csv
import jwt

login = Blueprint('login', __name__)

path_users = r'data/users.csv'

def encode_jwt(row):
    key = "Caesar"
    payload = {"username": row["username"], "user_id": row["id"], "role": row["role"], "expire": time.time()+3600}
    encoded_payload = jwt.encode(payload, key)
    return encoded_payload

@login.route('/', methods=['POST'])
def user_login():
    try:
        username = request.json["username"]
        password = request.json["password"]
    except KeyError:
        return json.dumps({"message": "username or password not entered"})

    li_userLogin = li_dictObject(path_users)
    for row in li_userLogin:
        if row["username"] == username and row["password"] == password:
            encoded_payload = encode_jwt(row)
            
            return json.dumps({"auth_token": encoded_payload.decode(),
                               "message": "user logged in"})
    return json.dumps({"message": "invalid username or password"})