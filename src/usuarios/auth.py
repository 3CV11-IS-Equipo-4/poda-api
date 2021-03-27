import jwt
import datetime

def encode_auth_token_usuario(usuario_email, SECRET_KEY):
    """
    Genera el token de autenticación para un usuario.
    """

    try:
        payload = {
            'exp' :  datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat' : datetime.datetime.utcnow(),
            'sub' : usuario_email
        }

        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return e

def decode_auth_token_usuario(auth_token, SECRET_KEY):
    """
    Decodifica un token de autenticación para un usuario.
    """
    try:
        payliad = jwt.decode(auth_token, SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
