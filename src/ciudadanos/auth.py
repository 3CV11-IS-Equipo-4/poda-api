import jwt
import datetime

def encode_auth_token_ciudadano(ciudadano_email, SECRET_KEY):
    """
    Genera el token de autenticación para un ciudadano.
    """

    try:
        payload = {
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat' : datetime.datetime.utcnow(),
            'sub' : ciudadano_email
        }
        
        return jwt.encode(payload, SECRET_KEY, algorithm='ES256')
    except Exception as e:
        return e

def decode_auth_token_ciudadano(auth_token, SECRET_KEY):
    """
    Decodifica un token de autenticación para un ciudadano.
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['ES256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return -1
    except jwt.InvalidTokenError:
        return -2
