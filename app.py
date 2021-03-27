from flask import Flask, jsonify, request 
from flask_cors import CORS 
import pymongo 
import os


app = Flask(__name__) 

CONNECTION_URL = os.environ.get('CONNECTION_URL')
DB_NAME = os.environ.get('DB_NAME')

print(CONNECTION_URL)


if CONNECTION_URL[0] == chr(34) and CONNECTION_URL[-1] == chr(34):
	client = pymongo.MongoClient(CONNECTION_URL[1:-1]) 
else:
	client = pymongo.MongoClient(CONNECTION_URL) 


# Database
try:
	Database = client.get_database(DB_NAME) 
except:
	Database = 'Example'

# Table 
SampleTable = Database.SampleTable 
ciudadano_tabla = Database.Ciudadano
solicitud_tabla = Database.Solicitud

@app.route('/')
def inicial():
	return 'La API está funcionando'

@app.route('/miruta/<name>')
def inicialPrueba(name):
	return 'Mi nombre es: '+name

# To insert a single document into the database, 
# insert_one() function is used localhost:3000/insert-one/mali/1/
@app.route('/insert-one/<name>/<id>/', methods=['GET']) 
def insertOne(name, id): 
	queryObject = {
		'Name': name, 
		'ID': id
	} 
	query = SampleTable.insert_one(queryObject) 
	return "Query inserted...!!!"

# To find the first document that matches a defined query, 
# find_one function is used and the query to match is passed 
# as an argument. 
@app.route('/find-one/<argument>/<value>/', methods=['GET']) 
def findOne(argument, value): 
	queryObject = {argument: value} 
	query = SampleTable.find_one(queryObject) 
	query.pop('_id') 
	return jsonify(query) 

# To find all the entries/documents in a table/collection, 
# find() function is used. If you want to find all the documents 
# that matches a certain query, you can pass a queryObject as an 
# argument. 
@app.route('/find/', methods=['GET']) 
def findAll(): 
	query = SampleTable.find() 
	output = {} 
	i = 0
	for x in query: 
		output[i] = x 
		output[i].pop('_id') 
		i += 1
	return jsonify(output) 


# To update a document in a collection, update_one() 
# function is used. The queryObject to find the document is passed as 
# the first argument, the corresponding updateObject is passed as the 
# second argument under the '$set' index. 
@app.route('/update/<key>/<value>/<element>/<updateValue>/', methods=['GET']) 
def update(key, value, element, updateValue): 
	queryObject = {key: value} 
	updateObject = {element: updateValue} 
	query = SampleTable.update_one(queryObject, {'$set': updateObject}) 
	if query.acknowledged: 
		return "Update Successful"
	else: 
		return "Update Unsuccessful"


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
