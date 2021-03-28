from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
import pymongo 
import os

#Blueprints
from src.solicitudes.solicitudes import construir_bp_solicitudes
from src.usuarios.usuarios import construir_bp_usuarios
from src.ciudadanos.ciudadanos import construir_bp_ciudadanos

app = Flask(__name__) 

CONNECTION_URL = os.environ.get('CONNECTION_URL')
DB_NAME = os.environ.get('DB_NAME')


if CONNECTION_URL[0] == chr(34) and CONNECTION_URL[-1] == chr(34):
	client = pymongo.MongoClient(CONNECTION_URL[1:-1]) 
else:
	client = pymongo.MongoClient(CONNECTION_URL) 

# Database
try:
	Database = client.get_database(DB_NAME) 
except:
	Database = 'Example'

# Manejo de CORS
CORS(app, supoort_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

#Manejor de Login
app.secret_key = b'*\x90\x85u\xf6p"\x97\x1a=<\xa2&JF\xf7'

# Table 
solicitud_tabla = Database.Solicitud
usuario_tabla = Database.Usuario

app.register_blueprint(construir_bp_solicitudes(client, Database, app.secret_key))
app.register_blueprint(construir_bp_usuarios(client, Database, app.secret_key))
app.register_blueprint(construir_bp_ciudadanos(client, Database, app.secret_key))

@app.route('/')
def inicial():
	print(request.headers)
	return 'La API está funcionando'
"""
#Registrar usuarios.
@app.route('/usuarios/', methods=['POST'])
@cross_origin(supports_credentials=True)
def registrar_usuario():
	datos_entrada = request.json
	datos_finales_usuario = validaciones_insertar_usuario(datos_entrada)
	resultado = usuario_tabla.insert_one(datos_finales_usuario)
	datos_finales_usuario.pop('_id')
	datos_finales_usuario['_id'] = str(resultado.inserted_id)

	return datos_finales_usuario, 200
	
#Rutas de solicitud.

#Registrar solicitud.
@app.route('/solicitudes/', methods=['POST'])
@cross_origin(supports_credentials=True)
def registrar_solicitud():
	
	datos_entrada = request.json
	datos_finales_ciudadano, datos_finales_solicitud = validaciones_insertar_solicitud(datos_entrada)
	resultado = solicitud_tabla.insert_one(datos_finales_solicitud)
	datos_finales_solicitud.pop('_id')
	datos_finales_solicitud['_id'] = str(resultado.inserted_id)

	return datos_finales_solicitud, 200

#Consulta de solicitudes para ciudadanos.
@app.route('/solicitudes/ciudadanos/<email>', methods=['GET'])
@cross_origin(supports_credentials=True)
def consultar_solicitudes_ciudadano(email):

	resultado_query = solicitud_tabla.find({'email': email})
	resultado_filtrado = []
	for solicitud in resultado_query:
		temp__id = str(solicitud['_id'])
		solicitud['_id'] = temp__id
		resultado_filtrado.append(solicitud)
	
	return {'solicitudes': resultado_filtrado}, 200	
"""

if __name__ == '__main__': 
	app.run(host='0.0.0.0', port=8000, debug=True) 
