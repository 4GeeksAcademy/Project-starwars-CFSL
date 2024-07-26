"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Personajes, Vehiculos, Planetas, Favoritos
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200

#[GET] /people Listar todos los registros de people en la base de datos.
@api.route('/all_people', methods=['GET'])
def get_all_people():
    people = Personajes.query.all()
    aux = list(map(lambda x: x.serialize(), people))
    return jsonify({'msg': 'OK', 'data': aux}), 200   

#[GET] /people/<int:people_id> Muestra la información de un solo personaje según su id.
@api.route('/one_people/<int:id>', methods=['GET'])
def get_one_people(id):
    people = Personajes.query.get(id)
    return jsonify({'msg': 'OK', 'personaje': people.serialize()}), 200

#[GET] /planets Listar todos los registros de planets en la base de datos.  
@api.route('/all_planets', methods=['GET'])
def get_all_planets():
    planetas = Planetas.query.all()
    aux = list(map(lambda x: x.serialize(), planetas))
    return jsonify({'msg': 'OK', 'data': aux}), 200    

#[GET] /planets/<int:planet_id> Muestra la información de un solo planeta según su id.  
@api.route('/one_planet/<int:id>', methods=['GET'])
def get_one_planet(id):
    planet = Planetas.query.get(id)
    return jsonify({'msg': 'OK', 'personaje': planet.serialize()}), 200

#[GET] /users Listar todos los usuarios del blog.
@api.route('/all_users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    print('\n')
    print('users sin serialize ----> ', users)
    print('\n')
    #users = [user.serialize() for user in users]
    #print( 'users CON serialize ----> ', users.serialize())
    # aux = []
    # for user in users:
    #     aux.append(user.serialize())
    aux = list(map(lambda x: x.serialize(), users))
    return jsonify({'msg': 'OK', 'data': aux}), 200

#[GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.
@api.route('/users/<int:user_id>/favoritos', methods=['GET'])
def get_user_favoritos(user_id):
    favoritos = Favoritos.query.filter_by(user_id=user_id).all()
    aux = [favorito.serialize() for favorito in favoritos]
    return jsonify({'msg': 'OK', 'data': aux}), 200

#[POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el id = planet_id.
@api.route('/favorito/planeta/<int:user_id>/<int:planet_id>', methods=['POST'])
def add_favorito_planeta(user_id, planet_id):
    user=User.query.get(user_id)
    planeta = Planetas.query.get(planet_id)

    if not user:
        return jsonify({'msg': 'User no encontrado'}), 404
    if not planeta:
        return jsonify({'msg': 'Planeta no encontrado'}), 404

    # Verificar si el favorito ya existe
    existe_fav = Favoritos.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existe_fav:
        return jsonify({'msg': 'Planeta ya existe en favoritos'}), 400

    # Crear y añadir el nuevo favorito
    new_favorito = Favoritos(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorito)
    db.session.commit()

    return jsonify({'msg': 'Planeta añadido a favoritos'}), 201

#[POST] /favorite/people/<int:people_id> Añade un nuevo people favorito al usuario actual con el id = people_id.
@api.route('/favorito/people/<int:user_id>/<int:people_id>', methods=['POST'])
def add_favorito_personaje(user_id, people_id):
    # Obtener usuario y personaje de la base de datos
    user = User.query.get(user_id)
    personaje = Personajes.query.get(people_id)

    # Verificar existencia del usuario
    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 404

    # Verificar existencia del personaje
    if not personaje:
        return jsonify({'msg': 'Personaje no encontrado'}), 404

    # Verificar si el personaje ya está en los favoritos del usuario
    existe_fav = Favoritos.query.filter_by(user_id=user_id, character_id=people_id).first()
    if existe_fav:
        return jsonify({'msg': 'Personaje ya está en los favoritos'}), 400

    # Crear y añadir el nuevo favorito
    new_favorito = Favoritos(user_id=user_id, character_id=people_id)
    db.session.add(new_favorito)
    db.session.commit()

    return jsonify({'msg': 'Personaje añadido a favoritos'}), 201

#[DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id.
@api.route('favorito/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def del_favorito_planeta(user_id, planet_id):
     # Obtener el favorito de la base de datos
    favorito = Favoritos.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    print(favorito)
    # Verificar si el favorito existe
    if not favorito:
        return jsonify({'msg': 'Favorito no encontrado'}), 404

    # Eliminar el favorito
    db.session.delete(favorito)
    db.session.commit()

    return jsonify({'msg': 'Planeta eliminado de favoritos'}), 200

#[DELETE] /favorite/people/<int:people_id> Elimina un people favorito con el id = people_id.
@api.route('favorito/people/<int:user_id>/<int:people_id>', methods=['DELETE'])
def del_favorito_people(user_id, people_id):
     # Obtener el favorito de la base de datos
    favorito = Favoritos.query.filter_by(user_id=user_id, character_id=people_id).first()
    print(favorito)
    # Verificar si el favorito existe
    if not favorito:
        return jsonify({'msg': 'Favorito no encontrado'}), 404

    # Eliminar el favorito
    db.session.delete(favorito)
    db.session.commit()

    return jsonify({'msg': 'Personaje eliminado de favoritos'}), 200