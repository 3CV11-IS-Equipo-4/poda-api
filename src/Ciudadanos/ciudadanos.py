from flask import Blueprint, request, make_response
from src.ciudadanos.auth import encode_auth_token_ciudadano, decode_auth_token_ciudadano
import pymongo
from pymongo.collection import ReturnDocument


def construir_bp_ciudadanos(cliente_mongo, Database, SECRET_KEY):
    ciudadanos_bp = Blueprint('ciudadanos_bp', __name__)

    ciudadano_tabla = Database.Ciudadano

    @ciudadanos_bp.route("/ciudadanos/login", methods=["POST"])
    def login_ciudadano():

        datos_entrada={}
        datos_entrada = request.json
        print(type(datos_entrada))
        print(datos_entrada) 

        if ("email" in datos_entrada.keys()) and ("password" in datos_entrada.keys()):
            registro_ciudadano = ciudadano_tabla.find_one(datos_entrada)
            if registro_ciudadano is not None:

                token = encode_auth_token_ciudadano(registro_ciudadano["email"], 
                                                    registro_ciudadano["nombres"], 
                                                    str(registro_ciudadano["_id"]),
                                                    registro_ciudadano["_id"] = str(registro_ciudadano["_id"]),
                                                    SECRET_KEY)

                resulting_response = make_response(({"autenticacion": True, "key": token}, 200, 
                {
                    'Access-Control-Allow-Origin': '*', 
                    'mimetype':'application/json'
                    }
                ))

                return resulting_response
            else:
                return make_response({"autenticacion": False}, 400, {
                    'Access-Control-Allow-Origin': '*', 
                    'mimetype':'application/json'
                    })
        else:
            return 'Acceso incorrecto'
    return ciudadanos_bp