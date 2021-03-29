import jwt
import datetime

def encode_auth_token_usuario(usuario_email, nombres, telefono, rol, permiso_administrador, usuario_id, SECRET_KEY):
    """
    Genera el token de autenticación para un usuario.
    """

    try:
        payload = {
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat' : datetime.datetime.utcnow(),
            'sub' : {
                "email" : usuario_email,
                "nombres" : nombres,
                "telefono" : telefono,
                "rol" : rol,
                "permiso_administrador" : permiso_administrador,
                "_id" : usuario_id

            }
        }
        
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return e

def decode_auth_token_usuario(auth_token, SECRET_KEY):
    """
    Decodifica un token de autenticación para un usuario.
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return -1
    except jwt.InvalidTokenError:
        return -2