import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from datetime import timedelta

from resources.user import UserRegister, Users, User
from resources.players import Player, Players
from resources.otkazan import Otkazan, Otkazani
from resources.drugari import Drugar, Drugari
from security import authenticate, identity

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.secret_key = 'secret123'
api = Api(app)



jwt = JWT(app, authenticate, identity)

# @jwt.auth_response_handler
# def customized_response_handler(access_token, identity):
#  return jsonify({
#  'access_token': access_token.decode('utf-8'),
#  'user_id': identity.id
#  })

api.add_resource(Player, '/player/<string:name>')
api.add_resource(Players, '/players')
api.add_resource(UserRegister, '/register')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<string:name>')
api.add_resource(Otkazani, '/otkazani')
api.add_resource(Otkazan, '/otkazan/<string:name>')
api.add_resource(Drugari, '/drugari')
api.add_resource(Drugar, '/drugar/<string:drugar>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
    