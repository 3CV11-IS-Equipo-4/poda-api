from flask import Blueprint, request, make_response
from src.ciudadano.auth import encode_auth_token_ciudadano
import pymongo

def construir_bp_ciudadano(cliente_mongo, Database, SECRET_KEY):
    ciudadano_bp = Blueprint('ciudadano_bp', __name__)

    ciudadano_tabla = Database.ciudadano

    @ciudadanos_bp.route("/login/ciudadanos", methods=["POST"])
    def login_ciudadano():

        datos_entrada = request.json
        print(type(datos_entrada))
        print(datos_entrada)

        registro_ciudadano = ciudadano_tabla.find_one(datos_entrada)
        if registro_ciudadano is not None:

            token = encode_auth_token_ciudadano(registro_ciudadano["email"], SECRET_KEY)

            respuesta_datos = {"nombres" : registro_ciudadano["nombres"],
                                "email" : registro_ciudadano["email"]
                                }

            resulting_response = make_response((respuesta_datos, 200, 
            {
                'Access-Control-Allow-Origin': '*', 
                'mimetype':'application/json',
                'x-access-token': token
                }
            ))

            return resulting_response
        else:
            return make_response({"autenticacion": False}, 400, {
                'Access-Control-Allow-Origin': '*', 
                'mimetype':'application/json'
                })

    return ciudadanos_bp