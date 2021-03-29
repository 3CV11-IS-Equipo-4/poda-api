import jwt
import datetime

def encode_auth_token_ciudadano(email, nombres, telefono, SECRET_KEY):

    try:
        payload = {
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat' : datetime.datetime.utcnow(),
            "sub" : {
                "email" : email,
                "nombres" : nombres,
                "telefono" : telefono
            }
        }

        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    except Exception as e:
        return e

def decode_auth_token_ciudadano(auth_token, SECRET_KEY):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return -1
    except jwt.InvalidTokenError:
        return -2