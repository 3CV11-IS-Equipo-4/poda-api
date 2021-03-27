from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
import pymongo 
import os
from validaciones_solicitud import validaciones_insertar_solicitud
from validaciones_usuario import validaciones_insertar_usuario

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

@app.route('/')
def inicial():
	print(request.headers)
	return 'La API está funcionando'

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


#Consulta de solicitudes para trabajadores.
#@app.route('/solicitudes/usuarios/<email>', methods=['GET'])
#def consultar_solicitudes_usuarios(email):

#	informacion_usuario = usuario_tabla.find({'email': email})
#	print(informacion_usuario['alcaldia'])
	
#	return 'Hola', 200	

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

#Login
@app.route('/login/', methods=['POST'])
@cross_origin(supports_credentials=True)
def iniciar_sesion():
	
	datos_inicio_sesion = request.json
	respuesta_datos = {}

	resultado = usuario_tabla.find_one({'email': datos_inicio_sesion['email'], 'password': datos_inicio_sesion['password']})

	print(resultado)
	permiso_admin = resultado['permiso_administrador']

	if resultado is not None:
		if permiso_admin:
			respuesta_datos = {'nombres': resultado['nombres'], 
								'apellido_paterno': resultado['apellido_paterno'],
								'apellido_materno': resultado['apellido_materno'], 
								'email': datos_inicio_sesion['email'],
								'permiso_administrador': True,
								'sesion_valida': True
								}
		else:
			respuesta_datos = {'nombres': resultado['nombres'], 
								'apellido_paterno': resultado['apellido_paterno'],
								'apellido_materno': resultado['apellido_materno'], 
								'email': datos_inicio_sesion['email'], 
								'sesion_valida': True, 
								'permiso_administrador': False,
								'rol': resultado['rol']
								}
	else:
		respuesta_datos = {'email': datos_inicio_sesion['email'], 'valido': False}
	
	return respuesta_datos, 200

<<<<<<< HEAD
#Consulta de solicitudes usuarios
@app.route('/solicitudes/<id>/', methods=['GET'])
def consultar_solicitudesCI(id):
	print(id)

	dato_ciudadano = ciudadano_tabla.find_one({'id':int(id)})
	#dato_ciudadano2 = ciudadano_tabla.find_one({'id':int(id)})
	#dato_ciudadano3 = ciudadano_tabla.find_one({'id':int(id)})
	#dato_ciudadano4 = ciudadano_tabla.find_one({'id':int(id)})
	
	print (dato_ciudadano)
	#print (dato2_ciudadano)
	#print (dato3_ciudadano)
	#print (dato4_ciudadano)
	nombre = dato_ciudadano ['nombre']
	#ap_pat = dato2_ciudadano ['apellido_paterno']
	#ap_mat = dato3_ciudadano ['apellido_materno']
	#email = dato4_ciudadano ['email']

	dato_solicitud = solicitud_tabla.find ({'nombre': nombre})
	#dato2_solicitud = solicitud_tabla.find ({'apellido_paterno': apellido paterno})
	#dato3_solicitud = solicitud_tabla.find ({'apellido_materno': apellido materno})
	#dato4_solicitud = solicitud_tabla.find ({'email': email})
	

	for registro in dato_solicitud: 
		print (registro)
	return "Los datos del usuarios son los siguientes"


#Rutas de solicitud.
@app.route('/solicitudes/', methods=['POST'])
def registrar_solicitud():
	
	datos_entrada = request.json
	datos_finales_ciudadano, datos_finales_solicitud = validaciones_insertar_solicitud(datos_entrada)
	resultado = solicitud_tabla.insert_one(datos_finales_solicitud)
	datos_finales_solicitud.pop('_id')
	datos_finales_solicitud['_id'] = str(resultado.inserted_id)

	return datos_finales_solicitud, 200


#Inicio de Sesión
@app.route('/IniciarSesion/', methods=['POST'])
def inciar_sesion():

	datos_entrada = request.json
	if email =True:
		password = True:
			return "Inicio de sesion exitoso"
		if
			return "Correo electronico o Password incorrectos"
		elif
			return "Usuario no encontrado"

if __name__ == '__main__':
	app.run(debug=True)
=======
if __name__ == '__main__': 
	app.run(host='0.0.0.0', port=8000, debug=True) 
>>>>>>> Tona
