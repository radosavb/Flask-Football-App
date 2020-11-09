import sqlite3
from flask_restful import Resource, reqparse
from flask import request
from models.user import UserModel
from flask_jwt import jwt_required

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This is mandatory field')
    parser.add_argument('password', type=str, required=True, help='This is mandatory field')
    
    def post(self):
        req_data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(req_data['username']):
            return {'msg': 'User vec postoji'}, 400

        user = UserModel(**req_data)
        user.save_to_db()
        return{'msg': 'User uspesno kreiran'}

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help='This is mandatory field')

    def get(self, name):
        user = UserModel.query.filter_by(username=name).first()
        if user:
            return user.json()
        return {'msg': 'User nije pronadjen.'}

    def delete(self, name):
        korisnik = UserModel.find_by_username(name)
        if korisnik:
            korisnik.delete_from_db()
        return {'msg': 'Korisnik uspesno izbrisan.'}
    
    def put(self, name):
        req_data = User.parser.parse_args()
        korisnik = UserModel.find_by_username(name)
        if korisnik:
            korisnik.password = req_data.password
            korisnik.save_to_db()
            return({'msg': 'Sifra uspesno promenjena!!!'})
        return({'msg':'Korisnik ne postoji'})

class Users(Resource):
    @jwt_required()
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}