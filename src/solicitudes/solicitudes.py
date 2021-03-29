from flask import Blueprint, request, make_response
from pymongo.collection import ReturnDocument
from src.solicitudes.validaciones_solicitud import validaciones_insertar_solicitud
from src.usuarios.auth import decode_auth_token_usuario
from src.ciudadanos.auth import decode_auth_token_ciudadano
from bson.objectid import ObjectId

def construir_bp_solicitudes(cliente_mongo, Database, SECRET_KEY):

    solicitudes_bp = Blueprint('solicitudes_bp', __name__)

    solicitud_tabla = Database.Solicitud
    usuario_tabla = Database.Usuario
    ciudadano_tabla = Database.Ciudadano

    @solicitudes_bp.route("/solicitudes/usuarios/", methods=["GET"])
    def consultar_solicitudes_usuario():

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
            usuario_datos = usuario_tabla.find_one({"email": decoded_token["email"]})
            solicitudes_realizadas = solicitud_tabla.find({"alcaldia_arbol":usuario_datos["alcaldia"]})

            datos_filtrados_solicitudes = {"solicitudes" : []}
            for solicitud in solicitudes_realizadas:
                temp__id = str(solicitud["_id"])
                solicitud["_id"] = temp__id
                datos_filtrados_solicitudes["solicitudes"].append(solicitud)

            resulting_response = make_response((datos_filtrados_solicitudes, 200, 
                                                {'Access-Control-Allow-Origin': '*', 
                                                'mimetype':'application/json',
                                                'x-access-token': request.headers["x-access-token"]}))

            return resulting_response

    @solicitudes_bp.route("/solicitudes/ciudadanos/", methods=["GET"])
    def consultar_solicitudes_ciudadanos():

        decoded_token = decode_auth_token_ciudadano(request.headers["x-access-token"], SECRET_KEY)
        if decoded_token == -1:
            return make_response({"error" : "Sesión expirada."}, 
                                 400, 
                                 {'Access-Control-Allow-Origin': '*', 
                                    'mimetype':'application/json'})
        elif decoded_token == -2:
            return make_response({"error" : "Ciudadano inválido"}, 
                                 400, 
                                 {'Access-Control-Allow-Origin': '*', 
                                    'mimetype':'application/json'})
        else:
            ciudadano_datos = ciudadano_tabla.find_one({"email": decoded_token["email"]})
            
            solicitudes_ciudadano = solicitud_tabla.find({"email":ciudadano_datos["email"]})

            datos_filtrados_solicitudes = {"solicitudes" : []}

            if solicitudes_ciudadano is not None:
                for solicitud in solicitudes_ciudadano:
                    temp__id = str(solicitud["_id"])
                    solicitud["_id"] = temp__id
                    datos_filtrados_solicitudes["solicitudes"].append(solicitud)

            resulting_response = make_response((datos_filtrados_solicitudes, 200, 
                                                {'Access-Control-Allow-Origin': '*', 
                                                'mimetype':'application/json',
                                                'x-access-token': request.headers["x-access-token"]}))

            return resulting_response
    
    @solicitudes_bp.route("/solicitudes/ciudadanos/<folio>", methods=["GET"])
    def consultar_solicitud_especifica_ciudadano(folio):

        decoded_token = decode_auth_token_ciudadano(request.headers["x-access-token"], SECRET_KEY)
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
            ciudadano_Datos = ciudadano_tabla.find_one({"email": decoded_token})

            solicitud_encontrada = solicitud_tabla.find_one({"folio" : int(folio), "email" : decoded_token["email"]})    

            solicitud_filtrada = {}
            for key in solicitud_encontrada:
                solicitud_filtrada[key] = solicitud_encontrada[key]
            
            solicitud_filtrada.pop('_id')
            solicitud_filtrada['_id'] = str(solicitud_encontrada['_id'])

            resulting_response = make_response((solicitud_filtrada, 200, 
                                                {'Access-Control-Allow-Origin': '*', 
                                                'mimetype':'application/json',
                                                'x-access-token': request.headers["x-access-token"]}))

            return resulting_response        


    @solicitudes_bp.route("/solicitudes/<id>", methods=["PATCH", "GET"])
    def aceptar_solicitud(id):

        if "x-access-token" in request.headers:
            
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
                if request.method == "PATCH":
                    usuario_datos = usuario_tabla.find_one({"email": decoded_token["email"]})

                    datos_solicitud = solicitud_tabla.find_one({"_id" : ObjectId("6060d7bbb2f46ad8bd9d1c3c")})

                    datos_entrada = request.json
                    if datos_entrada["aceptada"]:
                        
                        nuevo_estado = ""

                        if usuario_datos["rol"] == "ROP" and datos_solicitud["estado"] == "En revision de documentos por oficialía de partes":
                            nuevo_estado = "En revisión de documentos por Jefe de Área"
                        elif usuario_datos["rol"] == "JA" and datos_solicitud["estado"] == "En revisión de documentos por Jefe de Área":
                            nuevo_estado = "En revisión de información por Dictaminador"
                        elif usuario_datos["rol"] == "DI" and datos_solicitud["estado"] == "En revisión de información por Dictaminador":
                            if datos_solicitud["tipo_de_servicio"] == "Poda":
                                nuevo_estado = "Poda de árbol aceptada"
                            elif datos_solicitud["tipo_de_servicio"] == "Derribo":
                                nuevo_estado = "Derribo de árbol aceptado"  

                        else:
                            resulting_response = make_response(({"error" : "No tienes permiso para realizar esa acción."}, 400, 
                                                                {'Access-Control-Allow-Origin': '*', 
                                                                'mimetype':'application/json',
                                                                'x-access-token': request.headers["x-access-token"]}))
                            return resulting_response

                        solicitud_actualizada = solicitud_tabla.find_one_and_update(
                                                {"_id" : ObjectId("6060d7bbb2f46ad8bd9d1c3c")}, 
                                                {"$set" : {"estado" : nuevo_estado}},
                                                return_document=ReturnDocument.AFTER
                                            )
                        
                    else:
                        solicitud_actualizada = solicitud_tabla.find_one_and_update(
                                                {"_id" : ObjectId("6060d7bbb2f46ad8bd9d1c3c")}, 
                                                {"$set" : {"estado" : "Solicitud rechazada"}},
                                                return_document=ReturnDocument.AFTER
                                            )

                    registro_actualizado = {}
                    for key in solicitud_actualizada:
                        registro_actualizado[key] = solicitud_actualizada[key]
                    
                    registro_actualizado.pop('_id')
                    registro_actualizado['_id'] = str(solicitud_actualizada['_id'])

                    resulting_response = make_response((registro_actualizado, 200, 
                                                        {'Access-Control-Allow-Origin': '*', 
                                                        'mimetype':'application/json',
                                                        'x-access-token': request.headers["x-access-token"]}))

                    return resulting_response                
                else:
                    #Método GET.
                    usuario_datos = usuario_tabla.find_one({"email": decoded_token["email"]})

                    solicitud_encontrada = solicitud_tabla.find_one({"_id" : ObjectId("6060d7bbb2f46ad8bd9d1c3c")})    

                    solicitud_filtrada = {}

                    if solicitud_encontrada is not None:

                        for key in solicitud_encontrada:
                            solicitud_filtrada[key] = solicitud_encontrada[key]
                        
                        solicitud_filtrada.pop('_id')
                        solicitud_filtrada['_id'] = str(solicitud_encontrada['_id'])

                    resulting_response = make_response((solicitud_filtrada, 200, 
                                                        {'Access-Control-Allow-Origin': '*', 
                                                        'mimetype':'application/json',
                                                        'x-access-token': request.headers["x-access-token"]}))

                    return resulting_response                    

        else:
            return make_response({"error" : "Usuario inválido"}, 
                                400, 
                                {'Access-Control-Allow-Origin': '*', 
                                    'mimetype':'application/json'})

    @solicitudes_bp.route("/solicitudes/", methods=["POST"])
    def registrar_solictud():
        
        datos_entrada = request.json
        solicitud, ciudadano, datos_faltantes = validaciones_insertar_solicitud(datos_entrada)

        if len(datos_faltantes) == 0:
            solicitud["estado"] = "En revision de documentos por oficialía de partes"

            folio_maximo = solicitud_tabla.find_one(sort=[("folio", -1)])

            if folio_maximo is None:
                solicitud["folio"] = 1
            else:
                solicitud["folio"] = folio_maximo["folio"] + 1

            resulting_query = solicitud_tabla.insert_one(solicitud)
            solicitud.pop('_id')
            solicitud['_id'] = str(resulting_query.inserted_id)

            busqueda_ciudadano = ciudadano_tabla.find_one({"email" : ciudadano["email"]})
            if busqueda_ciudadano is None:
                ciudadano["password"] = str(ciudadano["codigo_postal"]) + str(solicitud["folio"]) 
                ciudadano_tabla.insert_one(ciudadano)
            
            resulting_response = make_response((solicitud, 201, {'Access-Control-Allow-Origin': '*', 'mimetype':'application/json'}))
            return resulting_response

        else:
            response_content = {"datos_faltantes" : datos_faltantes}
            resulting_response = make_response((response_content, 400, {'Access-Control-Allow-Origin': '*', 'mimetype':'application/json'}))
            return resulting_response

    return solicitudes_bp