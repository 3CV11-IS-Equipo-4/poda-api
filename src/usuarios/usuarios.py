from flask import Blueprint, request, make_response
from src.usuarios.auth import encode_auth_token_usuario, decode_auth_token_usuario
from src.control import verificar_authorization
from src.usuarios.validaciones_usuario import validaciones_insertar_usuario
import pymongo
from pymongo.collection import ObjectId, ReturnDocument

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


    @usuarios_bp.route("/usuarios/<id>", methods=["GET", "PATCH"])
    def manejar_usuario(id):

        autorizacion = verificar_authorization(request)
        if len(autorizacion) != 0:
            return autorizacion

        decoded_token = decode_auth_token_usuario(request.headers["Authorization"].split()[1], SECRET_KEY)
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

                    if not ObjectId.is_valid(id):
                        resulting_response = make_response(({"error" : "Usuario no encontrado."}, 400, 
                                                            {'Access-Control-Allow-Origin': '*', 
                                                            'mimetype':'application/json'
                                                            }))
                    else:                       
                        usuario_encontrado = usuario_tabla.find_one({"_id" : ObjectId(id)})
                        if usuario_encontrado is None:
                            resulting_response = make_response(({"error" : "Usuario no encontrado."}, 400, 
                                                                {'Access-Control-Allow-Origin': '*', 
                                                                'mimetype':'application/json'
                                                                }))                        
                        else:
                            usuario_filtrado = {}
                            for key in usuario_encontrado:
                                usuario_filtrado[key] = usuario_encontrado[key]
                            
                            usuario_filtrado.pop('_id')
                            usuario_filtrado['_id'] = str(usuario_encontrado['_id'])

                            resulting_response = make_response((usuario_filtrado, 200, 
                                                                {'Access-Control-Allow-Origin': '*', 
                                                                'mimetype':'application/json'
                                                                }))

                    return resulting_response

                elif request.method == "PATCH":
                    
                    if not ObjectId.is_valid(id):
                        resulting_response = make_response(({"error" : "Usuario no encontrado."}, 400, 
                                                            {'Access-Control-Allow-Origin': '*', 
                                                            'mimetype':'application/json'
                                                            }))
                    else:
                        if request.data:      

                            datos_entrada = request.json
                            usuario_actualizado = usuario_tabla.find_one_and_update(
                                                    {"_id" : ObjectId(id)},
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
                            registro_actualizado.pop("password")  

                            resulting_response = make_response((registro_actualizado, 200, 
                                                                {'Access-Control-Allow-Origin': '*', 
                                                                'mimetype':'application/json'} ))
                        else:
                            resulting_response = make_response(({"error" : "Información faltante"}, 400, 
                                                                {'Access-Control-Allow-Origin': '*', 
                                                                'mimetype':'application/json'} ))                            

            else:
                resulting_response = make_response(({"error" : "No tienes permiso de administrador."}, 200, 
                                                    {'Access-Control-Allow-Origin': '*', 
                                                    'mimetype':'application/json'}))          

            return resulting_response     

    @usuarios_bp.route("/usuarios/", methods=["GET"])
    def consultar_usuarios():

        autorizacion = verificar_authorization(request)
        if len(autorizacion) != 0:
            return autorizacion

        decoded_token = decode_auth_token_usuario(request.headers["Authorization"].split()[1], SECRET_KEY)
        if decoded_token == -1:
            body = {"error" : "Sesión expirada"}
            codigo_respuesta = 400
        elif decoded_token == -2:
            body = {"error" : "Usuario inválido."}
            codigo_respuesta = 400
        else:
            if decoded_token["permiso_administrador"]:
                usuarios_datos = usuario_tabla.find()

                datos_filtrados_usuarios = {"usuarios" : []}

                if usuarios_datos is not None:
                    for usuario in usuarios_datos:
                        temp__id = str(usuario["_id"])
                        usuario["_id"] = temp__id
                        datos_filtrados_usuarios["usuarios"].append(usuario)
                        datos_filtrados_usuarios["usuarios"][-1].pop("password")

                body = datos_filtrados_usuarios  
                codigo_respuesta = 200               

            else:
                body = {"error" : "No tienes permiso."}
                codigo_respuesta = 400

        return make_response((body, codigo_respuesta,{
                        'Access-Control-Allow-Origin': '*', 
                        'mimetype':'application/json'
                        }))      

    """@usuarios_bp.route("/usuarios", methods=["GET"])
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
    """
    
    @usuarios_bp.route('/usuarios/', methods=['POST'])
    def registrar_usuario():
        
        autorizacion = verificar_authorization(request)
        if len(autorizacion) != 0:
            return autorizacion

        decoded_token = decode_auth_token_usuario(request.headers["Authorization"].split()[1], SECRET_KEY)
        if decoded_token == -1:
            body = {"error" : "Sesión expirada"}
            codigo_respuesta = 400
        elif decoded_token == -2:
            body = {"error" : "Usuario inválido."}
            codigo_respuesta = 400
        else:
            if decoded_token["permiso_administrador"]:        

                if request.data:

                    datos_entrada = request.json 
                    datos_finales_usuario, datos_faltantes = validaciones_insertar_usuario(datos_entrada)

                    if len(datos_faltantes) > 0:
                        body = {"error" : "Datos faltantes.", "datos_faltantes" : datos_faltantes}
                        codigo_respuesta = 400
                    else:

                        usuario_correo_anterior = usuario_tabla.find_one({"email" : datos_finales_usuario["email"]})
                        if usuario_correo_anterior is not None:
                            body = {"error" : "Ya existe un usuario con ese email."}
                            codigo_respuesta = 400
                        else:
                            datos_finales_usuario["usuario_activo"] = True
                            resultado = usuario_tabla.insert_one(datos_finales_usuario)                

                            datos_finales_usuario.pop('password')
                            datos_finales_usuario['_id'] = str(resultado.inserted_id)

                            body = datos_finales_usuario
                            codigo_respuesta = 200
            else:
                body = {"error" : "No tienes permiso para realizar esto."}
                codigo_respuesta = 400
        
        return make_response((body, codigo_respuesta, {
                        'Access-Control-Allow-Origin': '*', 
                        'mimetype':'application/json'
                        }))
    
    return usuarios_bp
