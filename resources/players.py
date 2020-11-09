from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.players import PlayerModel
from flask_jwt import jwt_required

class Player(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('position', type=str, required=True, help='This field cannot be blank')
   
    def get(self, name):
        player = PlayerModel.find_by_name(name)
        if player: 
            return player.json()
        return {'msg': 'Igrac nije pronadjen'}, 404

    @jwt_required()
    def post(self, name):
        if PlayerModel.find_by_name(name):
            return {'msg': f'Igrac sa imenom {name} vec postoji.'}, 400

        req_data = Player.parser.parse_args()

        player = PlayerModel(name, **req_data)

        try:
            player.save_to_db()
        except:
            return {'msg': 'An error occurred'}, 500
        
        return {'msg': 'Uspesno ste se prijavili za fudbal'}, 201

    def delete(self, name):
        player = PlayerModel.find_by_name(name)
        if player:
            player.delete_from_db()
        return {'msg': 'Uspesno ste se odjavili sa fudbala!'}

    
class Players(Resource):
    def get(self):
        return {'players': [player.json() for player in PlayerModel.query.all()]}
