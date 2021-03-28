from flask import Blueprint, request, make_response
from src.usuarios.auth import encode_auth_token_usuario
import pymongo

def construir_bp_usuarios(cliente_mongo, Database, SECRET_KEY):
    usuarios_bp = Blueprint('usuarios_bp', __name__)

    usuario_tabla = Database.Usuario

    @usuarios_bp.route("/login/usuarios", methods=["POST"])
    def login_usuario():

        datos_entrada = request.json
        print(type(datos_entrada))
        print(datos_entrada)

        registro_usuario = usuario_tabla.find_one(datos_entrada)
        if registro_usuario is not None:

            token = encode_auth_token_usuario(registro_usuario["email"], SECRET_KEY)

            respuesta_datos = {"nombres" : registro_usuario["nombres"],
                                "email" : registro_usuario["email"],
                                "permiso_administrador" : registro_usuario["permiso_administrador"],
                                "rol" : registro_usuario["rol"]
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

    return usuarios_bp

    #Registrar usuarios.
    @app.route('/usuarios/registrar', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def registrar_usuario():
        datos_entrada = request.json
        datos_finales_usuario = validaciones_insertar_usuario(datos_entrada)
        resultado = usuario_tabla.insert_one(datos_finales_usuario)
        datos_finales_usuario.pop('_id')
        datos_finales_usuario['_id'] = str(resultado.inserted_id)

        return datos_finales_usuario, 200
