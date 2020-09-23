from flask import Flask
from flask import Blueprint
from flask import request
import time
import json
import csv
from functions import *
from blueprint_login import login
from property_blueprint import property
from blueprint_activity import activity

app = Flask(__name__)
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(property, url_prefix='/property')
app.register_blueprint(activity, url_prefix='/activity')