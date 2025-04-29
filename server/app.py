#!/usr/bin/env python3
import ipdb
import os

from flask import Flask, make_response, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_bcrypt import Bcrypt

from models import db

app = Flask(__name__)
app.secret_key = os.urandom(16)

# configure a database connection to the local file tests.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests.db'

# disable modification tracking to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

# Creates a new instance of the Bcrypt class, passing in the Flask app as an argument into the Bcrypt class constructor. We will use Bcrypt to encrypt our passwords
bcrypt = Bcrypt(app)

api = Api(app)

# Resource classes go here
class Test(Resource):
    def get(self):
        response_body = {
            "message": "GET request successfully made!"
        }
        return make_response(response_body, 200)
    
    def post(self):
        response_body = {
            "message": "POST request successfully made!",
            "data_sent": request.json
        }
        return make_response(response_body, 201)
    
    def patch(self):
        response_body = {
            "message": "PATCH request successfully made!",
            "data_sent": request.json
        }
        return make_response(response_body, 200)
    
    def delete(self):
        response_body = {
            "message": "DELETE request successfully made!"
        }
        return make_response(response_body, 200)
    
api.add_resource(Test, "/tests")

if __name__ == "__main__":
    app.run(port=7777, debug=True)