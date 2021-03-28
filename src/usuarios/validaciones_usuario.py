def validaciones_insertar_usuario(request):
    
    informacion_usuario = {}

    informacion_usuario['nombres'] = request['nombres']
    informacion_usuario['apellido_paterno'] = request['apellido_paterno']
    informacion_usuario['apellido_materno'] = request['apellido_materno']
    informacion_usuario['email'] = request['email']
    informacion_usuario['password'] = request['password']
    informacion_usuario['rol'] = request['rol']
    informacion_usuario['permiso_administrador'] = request['permiso_administrador']
    informacion_usuario['alcaldia'] = request['alcaldia']

    return informacion_usuario