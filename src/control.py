def verificar_authorization(request):

    if "Authorization" not in request.headers:
        return ({"error" : "Autorización inválida."}, 400, 
                                {'Access-Control-Allow-Origin': '*', 
                                'mimetype':'application/json'})
    else:
        contenido_authorization = request.headers["Authorization"].split()
        if len(contenido_authorization) != 2 or contenido_authorization[0] != "Bearer":
            return ({"error" : "Autorización inválida."}, 400, 
                                    {'Access-Control-Allow-Origin': '*', 
                                    'mimetype':'application/json'})
        else:
            return tuple()