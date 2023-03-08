from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from Models import db, User, Whiskey, whiskey_schema, whiskeys_schema 

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/whiskey', methods = ['POST'])
@token_required
def create_whiskey(current_user_token):
    name = request.json['name']
    brand = request.json['brand']
    type = request.json['type']
    age = request.json['age']
    size = request.json['size']
    alcohol_content = request.json['alcohol_content']
    user_token = current_user_token.token

    whiskey = Whiskey(name, brand, type, age, size, alcohol_content, user_token=user_token )

    db.session.add(whiskey)
    db.session.commit()

    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey', methods = ['GET'])
@token_required
def get_whiskey(current_user_token):
    a_user = current_user_token.token
    whiskeys =  Whiskey.query.filter_by(user_token = a_user).all()
    response = whiskeys_schema.dump(whiskeys)
    return jsonify(response)

@api.route('/whiskey/<id>', methods = ['GET'])
@token_required
def get_single_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)
    

@api.route('/whiskey/<id>', methods = ['POST', 'PUT'])
@token_required
def update_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    whiskey.name = request.json['name']
    whiskey.brand = request.json['brand']
    whiskey.type = request.json['type']
    whiskey.age = request.json['age']
    whiskey.size = request.json['size']
    whiskey.alcohol_content = request.json['alcohol_content']
    whiskey.user_token = current_user_token.token

    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey/<id>', methods = ['DELETE'])
@token_required
def delete_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    
    db.session.delete(whiskey)
    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)