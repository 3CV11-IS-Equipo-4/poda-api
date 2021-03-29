from flask import Blueprint, request, make_response
from src.ciudadanos.auth import encode_auth_token_ciudadano

def construir_bp_ciudadanos(cliente_mongo, Database, SECRET_KEY):
    ciudadanos_bp = Blueprint('ciudadanos_bp', __name__)

    ciudadano_tabla = Database.Ciudadano

        
    return ciudadanos_bp