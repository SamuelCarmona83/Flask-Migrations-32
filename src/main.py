"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Diario, Entrada
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello CCS 33!😜 "
    }

    return jsonify(response_body), 200


@app.route('/diaries', methods=['GET','POST'])
def handle_diaries():
    if(request.method=='GET'):
        all_diaries = Diario.query.all()
        return jsonify(
            [ diario.serialize() for diario in all_diaries]
        ), 200
    else:
        body = request.json
        if "autor" not in body:
            return 'No tiene autor!', 400
        if "nombre" not in body:
            return 'No tiene nombre', 400
        else:
            new_row = Diario.new_diary(body["nombre"], body["autor"])
            if new_row == None:
                return 'Un error ha ocurrido, upps!', 500
            else:
                return jsonify(new_row.serialize()), 200

@app.route('/diaries/<int:diary_id>', methods=['GET','PATCH','DELETE', 'PUT'])
def get_diary(diary_id):
    body = request.json
    search = Diario.query.get(diary_id)
    if request.method == 'GET':
        if search != None:
            return jsonify(search.serialize()), 200
        else:
            return 'No se encontro ese diario', 404
    elif request.method == 'PATCH':
        updated_diary = search.update(body["nombre"], body["autor"])
        if(updated_diary != False):
            return jsonify(updated_diary.serialize()), 200
        else:
            return 'No se pudo actualizar el diary', 500
    elif request.method == 'DELETE':
        result = search.delete()
        if result == True:
            return f'El diario {diary_id} ha sido eliminado con exito!', 200
        else:
            return 'Un error ha ocurrido, upps!', 500
    elif request.method == 'PUT':
        if "titulo" not in body:
            return 'No tiene autor!', 400
        if "contenido" not in body:
            return 'No tiene nombre', 400
        new = Entrada.new_entry(body["titulo"], body["contenido"], search)
        if new != None:
            return jsonify(new.serialize())
        else:
            return 'Un error ha ocurrido, upps!', 500
        return 'Eliminar un diario', 200




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
