from flask import Flask
from flask import Blueprint
from flask import request
from functions import *
import time
import json
import csv
import jwt


property = Blueprint('property', __name__)

path_property = 'data/property.csv'

def decode_auth_token(auth_token):
    key = "Caesar"
    try:
        data = jwt.decode(auth_token, key)
    except:
        return None
    return data

@property.route('/', methods=['GET'])
def get_property():
    li_property = li_dictObject(path_property)
    return json.dumps(li_property)


@property.route('/add', methods=['POST'])
def add_property():
    try:
        auth_token = request.json["auth_token"]
    except KeyError:
        return json.dumps({"message": "authorization not found"})

    key = "Caesar"
    data = jwt.decode(auth_token, key)
    if data["role"] == 'owner':
        try:
            id = request.json["id"]
            area = request.json["area"]
            no_of_bedrooms = request.json["no_of_bedrooms"]
            amenities = request.json["amenities"]
            furnishing = request.json["furnishing"]
            locality = request.json["locality"]
        except KeyError:
            return json.dumps({"message": "all fields needs to be entered"})
        header = ["id", "area", "no_of_bedrooms", "amenities",
                  "furnishing", "locality"]
        value = {"id": id, "area": area, "no_of_bedrooms": no_of_bedrooms,
                 "amenities": amenities, "furnishing": furnishing,
                 "locality": locality}
        append_row(path_property, header, value)
        return json.dumps({"message": "property added"})
    else:
        return json.dumps({"message": "not allowed to add property"})


@property.route('/update', methods=['POST'])
def update_property():
    try:
        auth_token = request.headers.get("auth_token")
    except KeyError:
        return json.dumps({"message": "authorization is not given"})
    
    data = decode_auth_token(auth_token)
    
    if data == None:
        return json.dumps({"status": False, "message": "invalid jwt"})
    
    if data["role"] == "owner" or data["role"] == "admin":
        try:
            property_id = request.json["id"]
            modifying_variable = request.json["modifying_variable"]
            modified_value = request.json["modified_value"]
        except KeyError:
            return json.dumps({"status": False, "message": "all fields needs to be entered"})

        li_property = li_dictObject(path_property)

        flag = False
        
        for row in li_property:
            print(row)
            print('--------------')
            if row["id"] == property_id:
                if row["owner_id"] == data["user_id"]:
                    
                    row[modifying_variable] = modified_value
                    overwrite_file(path_property, li_property)
                    flag = True
                    break
                else:
                    return json.dumps({"status": False, "message": "owner not allowed to change this property"})
        
        if flag:
            return json.dumps({"status": True, "message": "updated"})
        else:
            return json.dumps({"status": False, "message": "no such property"})
    
    else:
        return json.dumps({"status": False, "message": "user not allowed to change or update property"})


@property.route('/delete', methods=["DELETE"])
def delete_property():
    try:
        auth_token = request.json["auth_token"]
    except KeyError:
        return json.dumps({"message": "no authorization"})
    finally:
        return json.dumps({"message": "login expired"})

    key = "Caesar"
    data = jwt.decode(auth_token, key)
    if data["role"] == "owner":
        try:
            id = request.json["id"]
        except KeyError:
            return json.dumps({"message": "enter all the fields"})
        li_property = li_dictObject(path_property)
        for row in li_property:
            if row["id"] == id:
                li_property.remove(row)
                overwrite_file(path_property, li_property)
                return json.dumps({"message": "property deleted"})
        return json.dumps({"message": "property not found"})
    else:
        return json.dumps({"message": "not allowed to delete property"})
        