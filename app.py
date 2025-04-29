#!/usr/bin/env python3

# import ipdb
import os

from flask import Flask, make_response, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_bcrypt import Bcrypt

from models import db, Fruit

app = Flask(__name__)
# app.secret_key = os.urandom(16)

# configure a database connection to the local file tests.db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests.db'

# Make sure to enter the following command in the terminal - necessary for os.environ.get('DATABASE_URI') to work!
# export DATABASE_URI=postgresql://test491:Lsd7HM36xEVxQXExntgrnv8qPgMq1Sss@dpg-d08gmn2li9vc739q6dmg-a.virginia-postgres.render.com/tests_db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

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
    
class AllFruits(Resource):
    def get(self):
        fruits = Fruit.query.all()
        response_body = [fruit.to_dict() for fruit in fruits]
        return make_response(response_body, 200)
    
    def post(self):
        fruit_name = request.json.get('name')

        try:
            new_fruit = Fruit(name=fruit_name)
            db.session.add(new_fruit)
            db.session.commit()
            response_body = new_fruit.to_dict()
            return make_response(response_body, 201)
        except TypeError as te:
            response_body = {
                "error": str(te)
            }
            return make_response(response_body, 422)
        except ValueError as ve:
            response_body = {
                "error": str(ve)
            }
            return make_response(response_body, 422)
        except:
            response_body = {
                "error": "Fruit name cannot be null!"
            }
            return make_response(response_body, 422)

class FruitByID(Resource):
    def get(self, id):
        fruit = db.session.get(Fruit, id)

        if fruit:
            response_body = fruit.to_dict()
            return make_response(response_body, 200)
        else:
            response_body = {
                "error": "Fruit Not Found!"
            }
            return make_response(response_body, 404)
        
    def patch(self, id):
        fruit = db.session.get(Fruit, id)

        if fruit:
            try:
                for attr in request.json:
                    setattr(fruit, attr, request.json[attr])
                
                db.session.commit()
                response_body = fruit.to_dict()
                return make_response(response_body, 200)
            except TypeError as te:
                response_body = {
                    "error": str(te)
                }
                return make_response(response_body, 422)
            except ValueError as ve:
                response_body = {
                    "error": str(ve)
                }
                return make_response(response_body, 422)
            except:
                response_body = {
                    "error": "Fruit must have a name!"
                }
                return make_response(response_body, 422)

        else:
            response_body = {
                "error": "Fruit Not Found!"
            }
            return make_response(response_body, 404)
        
    def delete(self, id):
        fruit = db.session.get(Fruit, id)

        if fruit:
            db.session.delete(fruit)
            db.session.commit()
            return make_response({}, 204)
        else:
            response_body = {
                "error": "Fruit Not Found!"
            }
            return make_response(response_body, 404)

api.add_resource(Test, "/tests")
api.add_resource(AllFruits, '/fruits')
api.add_resource(FruitByID, "/fruits/<int:id>")

if __name__ == "__main__":
    app.run(port=7777, debug=True)