from flask import Blueprint, request, make_response
from src.ciudadanos.auth import encode_auth_token_ciudadano
import pymongo


def construir_bp_ciudadanos(cliente_mongo, Database, SECRET_KEY):
    ciudadano_bp = Blueprint('ciudadano_bp', __name__)

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
                                                    registro_ciudadano["_id"],
                                                    SECRET_KEY)

                return make_response(({"autenticacion": True, "key" : token}, 200, {
                    'Access-Control-Allow-Origin': '*', 
                    'mimetype':'application/json'}))
            else:
                return make_response(({"autenticacion": False}, 400, {
                    'Access-Control-Allow-Origin': '*', 
                    'mimetype':'application/json'
                }))
        else:
            return make_response(({"autenticacion": False}, 400, {
                    'Access-Control-Allow-Origin': '*', 
                    'mimetype':'application/json'
                }))

    return ciudadanos_bp
