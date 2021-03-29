def validaciones_insertar_usuario(request):
    
    informacion_usuario = {}
    datos_faltantes = []

    if "nombres" in request.keys():
        informacion_usuario['nombres'] = request['nombres']
    else:
        datos_faltantes.append("nombres")

    if "apellido_paterno" in request.keys():
        informacion_usuario['apellido_paterno'] = request['apellido_paterno']
    else:
        datos_faltantes.append("apellido_paterno")

    if "apellido_materno" in request.keys():
        informacion_usuario['apellido_materno'] = request['apellido_materno']
    else:
        datos_faltantes.append("apellido_materno")        

    if "email" in request.keys():
        informacion_usuario["email"] = request["email"]
    else:
        datos_faltantes.append("email")
    
    if "telefono" in request.keys():
        informacion_usuario["telefono"] = request["telefono"]
    else:
        datos_faltantes.append("telefono")

    if "password" in request.keys():
        informacion_usuario["password"] = request["password"]
    else:
        datos_faltantes.append("password")

    if "alcaldia" in request.keys():
        informacion_usuario["alcaldia"] = request["alcaldia"]
    else:
        datos_faltantes.append("alcaldia")        
    
    if "rol" in request.keys():
        informacion_usuario["rol"] = request["rol"]
    else:
        datos_faltantes.append("rol")

    if "permiso_administrador" in request.keys():
        informacion_usuario["permiso_administrador"] = request["permiso_administrador"]
    else:
        datos_faltantes.append("permiso_administrador")        

    return informacion_usuario, datos_faltantes