from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
import pymongo 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

#Blueprints
from src.solicitudes.solicitudes import construir_bp_solicitudes
from src.usuarios.usuarios import construir_bp_usuarios

from src.ciudadanos.ciudadanos import construir_bp_ciudadanos

app = Flask(__name__) 

CONNECTION_URL = os.environ.get('CONNECTION_URL')
DB_NAME = os.environ.get('DB_NAME')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')


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
ciudadano_tabla = Database.Ciudadano

app.register_blueprint(construir_bp_solicitudes(client, Database, app.secret_key))
app.register_blueprint(construir_bp_usuarios(client, Database, app.secret_key))

app.register_blueprint(construir_bp_ciudadanos(client, Database, app.secret_key))


@app.route('/')
def inicial():
	print(request.headers)
	return 'La API está funcionando'

if __name__ == '__main__': 
	app.run(host='0.0.0.0', port=8000, debug=True) 
