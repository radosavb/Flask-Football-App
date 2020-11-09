import sqlite3
from flask_restful import Resource, reqparse
from flask import request
from models.drugari import DrugarModel
from flask_jwt import jwt_required

class Drugar(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This is mandatory field')
    parser.add_argument('position', type=str, required=True, help='This is mandatory field')

    @jwt_required()
    def post(self, drugar):        
        if DrugarModel.find_by_drugar(drugar):
            return {'message': 'Igrac sa ovim imenom je vec prijavljen'}, 400

        req_data = Drugar.parser.parse_args()

        drugar = DrugarModel(drugar, **req_data)

        try:
            drugar.save_to_db()            
        except:
            return {'message': 'An error occurred'}, 500

        return{'message': 'Prijavili ste drugara'}

    def delete(self, drugar):
        drugar = DrugarModel.find_by_drugar(drugar)
        if drugar:
            drugar.delete_from_db()
        return {'msg': 'Otkazali ste fudbal za drugara'}

class Drugari(Resource):
    def get(self):
        return {'drugari': [drugar.json() for drugar in DrugarModel.query.all()]}