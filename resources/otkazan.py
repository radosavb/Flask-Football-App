import sqlite3
from flask_restful import Resource, reqparse
from flask import request
from models.otkazan import OtkazanModel

class Otkazan(Resource):
    def post(self, name):
        if OtkazanModel.query.filter_by(username=name).first():
            return {'msg': 'User already exists'}
        user = OtkazanModel(name)
        user.save_to_db()
        return{'msg': 'Uspesno ste otkazali.'}

    def delete(self, name):
        player = OtkazanModel.find_by_username(name)
        if player:
            player.delete_from_db()
        return {'msg': 'Vratili ste se iz otkazanih.'}

class Otkazani(Resource):
    def get(self):
        return {'otkazani': [user.json() for user in OtkazanModel.query.all()]}