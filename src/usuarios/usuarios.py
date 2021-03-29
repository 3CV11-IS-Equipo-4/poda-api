from flask import Blueprint, request, make_response
from src.usuarios.auth import encode_auth_token_usuario, decode_auth_token_usuario
import pymongo
from pymongo.collection import ReturnDocument

def construir_bp_usuarios(cliente_mongo, Database, SECRET_KEY):
    usuarios_bp = Blueprint('usuarios_bp', __name__)

    usuario_tabla = Database.Usuario

    @usuarios_bp.route("/login/usuarios", methods=["POST"])
    def login_usuario():

        if request.data:
            datos_entrada = request.json

            if "email" in datos_entrada.keys() and "password" in datos_entrada.keys():

                registro_usuario = usuario_tabla.find_one(datos_entrada)
                if registro_usuario is not None:

                    token = encode_auth_token_usuario(registro_usuario["email"], registro_usuario["nombres"], 
                                                    registro_usuario["telefono"], registro_usuario["rol"], 
                                                    registro_usuario["permiso_administrador"], str(registro_usuario["_id"]), SECRET_KEY)

                    resulting_response = make_response(({"autenticacion": True, "key" : token }, 200, 
                    {
                        'Access-Control-Allow-Origin': '*', 
                        'mimetype':'application/json'
                        }
                    ))

                    return resulting_response
                    
        return make_response({"autenticacion": False}, 400, {
        'Access-Control-Allow-Origin': '*', 
        'mimetype':'application/json'
        })


    @usuarios_bp.route("/usuarios/<email>", methods=["GET", "PATCH"])
    def manejar_usuario(email):

        if "x-access-token" in  request.headers:

            decoded_token = decode_auth_token_usuario(request.headers["x-access-token"], SECRET_KEY)
            if decoded_token == -1:
                return make_response({"error" : "Sesión expirada."}, 
                                    400, 
                                    {'Access-Control-Allow-Origin': '*', 
                                        'mimetype':'application/json'})
            elif decoded_token == -2:
                return make_response({"error" : "Usuario inválido"}, 
                                    400, 
                                    {'Access-Control-Allow-Origin': '*', 
                                        'mimetype':'application/json'})
            else:

                if decoded_token["permiso_administrador"]:

                    if request.method == "GET":

                        usuario_encontrado = usuario_tabla.find_one({"email": decoded_token["email"]})  

                        usuario_filtrado = {}
                        for key in usuario_encontrado:
                            usuario_filtrado[key] = usuario_encontrado[key]
                        
                        usuario_filtrado.pop('_id')
                        usuario_filtrado['_id'] = str(usuario_encontrado['_id'])

                        resulting_response = make_response((usuario_filtrado, 200, 
                                                            {'Access-Control-Allow-Origin': '*', 
                                                            'mimetype':'application/json',
                                                            'x-access-token': request.headers["x-access-token"]}))

                        return resulting_response

                    elif request.method == "PATCH":
                        

                            datos_entrada = request.json

                            usuario_actualizado = usuario_tabla.find_one_and_update(
                                                    {"email" : email},
                                                    {"$set" : datos_entrada},
                                                    return_document=ReturnDocument.AFTER
                                                )

                            registro_actualizado = {}
                            for key in usuario_actualizado:
                                registro_actualizado[key] = usuario_actualizado[key]
                            
                            print("************************************************************")
                            print(usuario_actualizado)

                            registro_actualizado.pop('_id')
                            registro_actualizado['_id'] = str(usuario_actualizado['_id'])  

                            resulting_response = make_response((registro_actualizado, 200, 
                                                                {'Access-Control-Allow-Origin': '*', 
                                                                'mimetype':'application/json',
                                                                'x-access-token': request.headers["x-access-token"]} ))

                else:
                    resulting_response = make_response(({"error" : "No tienes permiso de administrador."}, 200, 
                                                        {'Access-Control-Allow-Origin': '*', 
                                                        'mimetype':'application/json',
                                                        'x-access-token': request.headers["x-access-token"]}))          

                return resulting_response
        else:
            print("Sin permiso. ):")
            resulting_response = make_response(({"error" : "No tienes permiso para realizar esta acción."}, 400, 
                                                {'Access-Control-Allow-Origin': '*', 
                                                'mimetype':'application/json'
                                                }))

            return resulting_response         

    @usuarios_bp.route("/usuarios", methods=["GET"])
    def consultar_usuarios():

        if "x-access-token" in request.headers:
            print("Sí hay token")
            decoded_token = decode_auth_token_usuario(request.headers["x-access-token"], SECRET_KEY)
            if decoded_token == -1:
                body = {"error" : "Sesión expirada"}
                codigo_respuesta = 400
            elif decoded_token == -2:
                body = {"error" : "Usuario inválido."}
                codigo_respuesta = 400
            else:
                print(decoded_token)
                if decoded_token["permiso_administrador"]:
                    usuarios_datos = usuario_tabla.find()

                    datos_filtrados_usuarios = {"usuarios" : []}

                    if usuarios_datos is not None:
                        for usuario in usuarios_datos:
                            temp__id = str(usuario["_id"])
                            usuario["_id"] = temp__id
                            datos_filtrados_usuarios["usuarios"].append(usuario)

                    body = datos_filtrados_usuarios  
                    codigo_respuesta = 200               

                else:
                    body = {"error" : "No tienes permiso."}
                    codigo_respuesta = 400
        else:
            body = {"error" : "No tienes permiso."}
            codigo_respuesta = 400

        return make_response((body, codigo_respuesta,{
                        'Access-Control-Allow-Origin': '*', 
                        'mimetype':'application/json'
                        }))

    return usuarios_bp
    
    @usuarios_bp.route('/usuarios/registrar', methods=['POST'])
    def registrar_usuario():
        
        datos_entrada = request.json
        print(type(datos_entrada))
        print(datos_entrada) 
        datos_finales_usuario = validaciones_usuario(datos_entrada)
        resultado = usuario_tabla.insert_one(datos_finales_usuario)
        datos_finales_usuario.pop('_id')
        datos_finales_usuario['_id'] = str(resultado.inserted_id)
        
        return datos_finales_usuario, 200
    
    return usuarios_bp
