from flask import Blueprint, request, make_response
from src.solicitudes.validaciones_solicitud import validaciones_insertar_solicitud

def construir_bp_solicitudes(cliente_mongo, Database):

    solicitudes_bo = Blueprint('solicitudes_bp', __name__)

    solicitud_tabla = Database.Solicitud

    @solicitudes_bo.route("/solicitudes/", methods=["POST"])
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

    return solicitudes_bo