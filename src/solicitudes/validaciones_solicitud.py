def validaciones_insertar_solicitud(request_data):
    print(type(request_data))

    solicitud = {}
    ciudadano = {}

    datos_faltantes = []

    if "nombres" in request_data.keys():
        solicitud["nombres"] = request_data["nombres"]
        ciudadano["nombres"] = request_data["nombres"]
    else:
        datos_faltantes.append("nombres")
    
    if "apellido_paterno" in request_data.keys():
        solicitud["apellido_paterno"] = request_data["apellido_paterno"]
        ciudadano["apellido_paterno"] = request_data["apellido_paterno"]
    else:
        datos_faltantes.append("apellido_paterno")

    if "apellido_materno" in request_data.keys():
        solicitud["apellido_materno"] = request_data["apellido_materno"]
        ciudadano["apellido_materno"] = request_data["apellido_materno"]
    else:
        datos_faltantes.append("apellido_materno")
    
    if "email" in request_data.keys():
        solicitud["email"] = request_data["email"]
        ciudadano["email"] = request_data["email"]
    else:
        datos_faltantes.append("email")

    if "numero_telefono" in request_data.keys():
        ciudadano["numero_telefono"] = request_data["numero_telefono"]
    else:
        datos_faltantes.append("numero_telefono")
    
    if "calle" in request_data.keys():
        ciudadano["calle"] = request_data["calle"]
    else:
        datos_faltantes.append("calle")
    
    if "numero_exterior" in request_data.keys():
        ciudadano["numero_exterior"] = request_data["numero_exterior"]
    else:
        datos_faltantes.append("numero_exterior")

    if "numero_interior" in request_data.keys():
        ciudadano["numero_interior"] = request_data["numero_interior"]
    else:
        ciudadano["numero_interio"] = "SN"
    
    if "codigo_postal" in  request_data.keys():
        ciudadano["codigo_postal"] = request_data["codigo_postal"]
    else:
        datos_faltantes.append("codigo_postal")

    if "documento_identificacion_oficial" in request_data.keys():
        ciudadano["documento_identificacion_oficial"] = request_data["documento_identificacion_oficial"] 
    else:
        datos_faltantes.append("documento_de_identificacion_oficial")

    if "tipo_de_servicio" in request_data.keys():
        solicitud["tipo_de_servicio"] = request_data["tipo_de_servicio"]
    else:
        datos_faltantes.append("tipo_de_servicio")

    if "calle_arbol" in request_data.keys():
        solicitud["calle_arbol"] = request_data["calle_arbol"]
    else:
        datos_faltantes.append("calle_arbol")
    
    if "colonia_arbol" in request_data.keys():
        solicitud["colonia_arbol"] = request_data["colonia_arbol"]
    else:
        datos_faltantes.append("colonia_arbol")

    if "alcaldia_arbol" in request_data.keys():
        solicitud["alcaldia_arbol"] = request_data["alcaldia_arbol"]
    else:
        datos_faltantes.append("alcaldia_arbol")
    
    if "calle_adyacente_1" in request_data.keys():
        solicitud["calle_adyacente_1"] = request_data["calle_adyacente_1"]
    else:
        datos_faltantes.append("calle_adyacente_1")

    if "calle_adyacente_2" in request_data.keys():
        solicitud["calle_adyacente_2"] = request_data["calle_adyacente_2"]
    else:
        datos_faltantes.append("calle_adyacente_2")

    if "referencias" in request_data.keys():
        solicitud["referencias"] = request_data["referencias"]
    else:
        datos_faltantes.append("referencias")
    
    if "motivos" in request_data.keys():
        solicitud["motivos"] = request_data["motivos"]
    else:
        datos_faltantes.append("motivos")
    
    if "fotos" in request_data.keys():
        if len(request_data["fotos"]) < 5:
            mensaje = "Hacen falta {} fotos".format((5 - len(request_data["fotos"])))
            datos_faltantes.append(mensaje)
        elif len(request_data["fotos"]) > 10:
            mensaje = "Sobran {} fotos".format((10 - len(request_data["fotos"])))
            datos_faltantes.append(mensaje)
        else:
            solicitud["fotos"] = request_data["fotos"]
    else:
        datos_faltantes.append("fotos")

    if "modalidad" in request_data.keys():
        solicitud["modalidad"] = request_data["modalidad"]

        if solicitud["modalidad"] == "propiedad-privada":

            if "privada" in request_data.keys():

                solicitud["privada"] = {}

                if "comprobante_domicilio" in request_data["privada"].keys():
                    solicitud["privada"]["comprobante_domicilio"] = request_data["privada"]["comprobante_domicilio"]
                else:
                    datos_faltantes.append("comprobante_domicilio")
                
                if "comprobante_propiedad" in request_data["privada"].keys():
                    solicitud["privada"]["comprobante_propiedad"] = request_data["privada"]["comprobante_propiedad"]
                else:
                    datos_faltantes.append("comprobante_propiedad")

                if "tipo_privada" in request_data["privada"].keys():
                    solicitud["privada"]["tipo_privada"] = request_data["privada"]["tipo_privada"]

                    if solicitud["privada"]["tipo_privada"] == "construccion":
                        
                        if "construccion" in request_data["privada"]:
                            
                            solicitud["privada"]["construccion"] = {}

                            if "documento_registro" in request_data["privada"]["construccion"].keys():
                                solicitud["privada"]["construccion"]["documento_registro"] = request_data["privada"]["construccion"]["documento_registro"]
                            else:
                                datos_faltantes.append("documento_registro")

                            if "documento_planos" in request_data["privada"]["construccion"].keys():
                                solicitud["privada"]["construccion"]["documento_planos"] = request_data["privada"]["construccion"]["documento_planos"]
                            else:
                                datos_faltantes.append("documento_planos")                                

                            if "documento_declaratoria" in request_data["privada"]["construccion"].keys():
                                solicitud["privada"]["construccion"]["documento_declaratoria"] = request_data["privada"]["construccion"]["documento_declaratoria"]
                            else:
                                datos_faltantes.append("documento_declaratoria")                                
                        else:
                            datos_faltantes.append("construccion")

                    elif solicitud["privada"]["tipo_privada"] == "riesgo":

                        solicitud["privada"]["riesgo"] = {}

                        if "documento_dictamen_riesgo" in request_data["privada"]["riesgo"].keys():
                                solicitud["privada"]["riesgo"]["documento_dictamen_riesgo"] = request_data["privada"]["riesgo"]["documento_dictamen_riesgo"]
                        else:
                            datos_faltantes.append("documento_dictamen_riesgo")
                else:
                    datos_faltantes.append("tipo_privada")
    
    else:
        datos_faltantes.append("modalidad")
    
    return solicitud, ciudadano, datos_faltantes


