from flask import Flask
from flask import Blueprint
from flask import request
from functions import *
import time
import json
import csv
import jwt

activity = Blueprint('activity', __name__)

path_userRequest = r'data\user_request.csv'
path_user = r'data\user_login.csv'
path_owner = r'data\owner_login.csv'
path_rented = r'data\rented.csv'


@activity.route('/rent', methods=['POST'])
def rent():
    try:
        auth_token = request.json["auth_token"]
    except KeyError:
        return json.dumps({"message": "no authorization"})
    finally:
        return json.dumps({"message": "login expired"})

    key = "Caesar"
    data = jwt.decode(auth_token, key)

    try:
        property_id = request.json["property_id"]
    except KeyError:
        return json.dumps({"message": "give the detail of property to be rented"})

    li_rent = li_dictObject(path_rented)
    header = li_rent[0].keys()
    id = int(li_rent[-1]["id"])+1
    value = {"id": str(id), "user_id": data["id"],
             "property_id": property_id}
    append_row(path_rented, header, value)
    return json.dumps({"message": "property rented"})


@activity.route('/get-in-touch', methods=['POST'])
def get_in_touch():
    try:
        auth_token = request.json["auth_token"]
    except KeyError:
        return json.dumps({"message": "auth0rization not given"})
    finally:
        return json.dumps({"message": "login expired"})

    key = "Caesar"
    data = jwt.decode(auth_token, key)

    try:
        owner_id = request.json["owner_id"]
    except KeyError:
        return json.dumps({"message": "field need to entered"})

    li_userRequest = li_dictObject(path_userRequest)
    header = li_userRequest[0].keys()
    id = int(li_userRequest[-1]["id"]) + 1
    value = {"id": id, "user_id": data["id"], "owner_id": owner_id}
    append_row(path_userRequest, header, value)
    return json.dumps({"message": "requested"})