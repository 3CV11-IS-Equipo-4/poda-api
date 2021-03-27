from flask import Blueprint, request, make_response
from src.solicitudes.validaciones_solicitud import validaciones_insertar_solicitud
from src.usuarios.auth import decode_auth_token_usuario

def construir_bp_solicitudes(cliente_mongo, Database, SECRET_KEY):

    solicitudes_bp = Blueprint('solicitudes_bp', __name__)

    solicitud_tabla = Database.Solicitud
    usuario_tabla = Database.Usuario

    @solicitudes_bp.route("/solicitudes/usuarios/", methods=["GET"])
    def consultar_solicitudes_usuario():
        print(request.headers["x-access-token"])

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
            usuario_datos = usuario_tabla.find_one({"email": decoded_token})
            solicitudes_alcaldia = solicitud_tabla.find({"alcaldia_arbol":usuario_datos["alcaldia"]})

            print(solicitudes_alcaldia)

            datos_filtrados_solicitudes = {"solicitudes" : []}
            for solicitud in solicitudes_alcaldia:
                temp__id = str(solicitud["_id"])
                solicitud["_id"] = temp__id
                datos_filtrados_solicitudes["solicitudes"].append(solicitud)

            resulting_response = make_response((datos_filtrados_solicitudes, 200, 
                                                {'Access-Control-Allow-Origin': '*', 
                                                'mimetype':'application/json',
                                                'x-access-token': request.headers["x-access-token"]}))

            return resulting_response

    @solicitudes_bp.route("/solicitudes/", methods=["POST"])
    def registrar_solictud():
        
        datos_entrada = request.json
        solicitud, ciudadano, datos_faltantes = validaciones_insertar_solicitud(datos_entrada)
        
        print(solicitud)

        if len(datos_faltantes) == 0:
            solicitud["estado"] = "En revision de documentos por oficialía de partes"
            resulting_query = solicitud_tabla.insert_one(solicitud)
            solicitud.pop('_id')
            solicitud['_id'] = str(resulting_query.inserted_id)
            
            resulting_response = make_response((solicitud, 201, {'Access-Control-Allow-Origin': '*', 'mimetype':'application/json'}))
            return resulting_response

        else:
            response_content = {"datos_faltantes" : datos_faltantes}
            print(response_content)
            resulting_response = make_response((response_content, 400, {'Access-Control-Allow-Origin': '*', 'mimetype':'application/json'}))
            return resulting_response

    return solicitudes_bp