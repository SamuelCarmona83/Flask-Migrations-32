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
from models import db, User, Diario
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
        )
    else:
        body = request.json
        if "autor" not in body:
            return 'No tiene autor!', 400
        if "nombre" not in body:
            return 'No tiene nombre', 400
        else:
            new_row = Diario.new_diary(body["nombre"], body["autor"])
            if new_row == None:
                return 'An error has occurd', 500
            else:
                return jsonify(new_row.serialize())





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
