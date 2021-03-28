from flask import Blueprint, request, make_response
from src.usuarios.auth import encode_auth_token_usuario
import pymongo

@usuarios_bp.route("/registrar/", methods=["POST"])
def registrar_usuario():

	datos_entrada = request.json
	datos_finales_usuario = validaciones_insertar_usuario(datos_entrada)
	resultado = usuario_tabla.insert_one(datos_finales_usuario)
	datos_finales_usuario.pop('_id')
	datos_finales_usuario['_id'] = str(resultado.inserted_id)

	return datos_finales_usuario, 200
    