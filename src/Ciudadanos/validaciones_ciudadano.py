def validaciones_insertar_ciudadano(request):
    
    informacion_ciudadano = {}

    informacion_ciudadano['nombres'] = request['nombres']
    informacion_ciudadano['apellido_paterno'] = request['apellido_paterno']
    informacion_ciudadano['apellido_materno'] = request['apellido_materno']
    informacion_ciudadano['email'] = request['email']
    informacion_ciudadano['password'] = request['password']
    informacion_ciudadano['telefono'] = request['telefono']
    informacion_ciudadano['calle'] = request['calle']
    informacion_ciudadano['colonia'] = request['colonia']
    informacion_ciudadano['alcaldia'] = request['alcaldia']
    informacion_ciudadano['numero_exterior'] = request['numero_exterior']
    informacion_ciudadano['codigo_postal'] = request['codigo_postal']
    informacion_ciudadano['_id'] = request ['_id']

    return informacion_ciudadano