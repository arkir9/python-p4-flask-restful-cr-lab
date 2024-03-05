#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_dicts = [plant.to_dict() for plant in plants]
        return plant_dicts, 200
    
    def post(self):
        # Extract data from the JSON request
        data = request.get_json()

        # Create a new plant record
        new_record = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )

        # Add the new record to the session and commit changes
        db.session.add(new_record)
        db.session.commit()

        # Prepare the response with the created record data
        response_dict = new_record.to_dict()
        return jsonify(response_dict), 201
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if plant:
            return plant.to_dict(), 200
        else:
            return {"error": "Plant not found"}, 404

api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
