import jwt
import datetime


def encode_auth_token_ciudadano(ciudadano_email, nombres, ciudadano_id, SECRET_KEY):

    """
    Genera el token de autenticación para un ciudadano.
    """

    try:
        payload = {
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat' : datetime.datetime.utcnow(),
            'sub' : {
                'email':ciudadano_email,
                'nombres': nombres,
                '_id': str(ciudadano_id)
                }
        }
        
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    except Exception as e:
        return e

def decode_auth_token_ciudadano(auth_token, SECRET_KEY):
    """
    Decodifica un token de autenticación para un ciudadano.
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])

        return payload['sub']
    except jwt.ExpiredSignatureError:
        return -1
    except jwt.InvalidTokenError:
        return -2
