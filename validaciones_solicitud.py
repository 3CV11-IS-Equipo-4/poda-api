def validaciones_insertar_solicitud(request):
    
    if isinstance(request, dict):

        nuevo_registro_solicitud = {}
        nuevo_registro_ciudadano = {}

        nuevo_registro_ciudadano["nombres"] = request["nombres"]
        nuevo_registro_ciudadano["apellido_paterno"] = request["apellido_paterno"]
        nuevo_registro_ciudadano["apellido_materno"] = request["apellido_materno"]
        nuevo_registro_ciudadano["email"] = request["email"]
        nuevo_registro_ciudadano["numero_telefono"] = request["numero_telefono"]
        nuevo_registro_ciudadano["calle"] = request["calle"]
        nuevo_registro_ciudadano["colonia"] = request["colonia"]
        nuevo_registro_ciudadano["numero_exterior"] = request["numero_exterior"]
        nuevo_registro_ciudadano["numero_interior"] = request["numero_interior"]
        nuevo_registro_ciudadano["codigo_postal"] = request["codigo_postal"]
        nuevo_registro_ciudadano["documento_identificacion_oficial"] = request["documento_identificacion_oficial"]

        nuevo_registro_solicitud["tipo_servicio"] = request["tipo_servicio"]
        nuevo_registro_solicitud["calle_arbol"] = request["calle_arbol"]
        nuevo_registro_solicitud["colonia_arbol"] = request["colonia_arbol"]
        nuevo_registro_solicitud["alcaldia_arbol"] = request["alcaldia_arbol"]
        nuevo_registro_solicitud["calle_adyacente_1"] = request["calle_adyacente_1"]
        nuevo_registro_solicitud["calle_adyacente_2"] = request["calle_adyacente_2"]
        nuevo_registro_solicitud["referencias"] = request["referencias"]
        nuevo_registro_solicitud["motivos"] = request["motivos"]
        nuevo_registro_solicitud["fotos"] = request["fotos"]
        nuevo_registro_solicitud["nombres"] = request["nombres"]
        nuevo_registro_solicitud["apellido_paterno"] = request["apellido_paterno"]
        nuevo_registro_solicitud["apellido_materno"] = request["apellido_materno"]
        nuevo_registro_solicitud["email"] = request["email"]          

        #if "nombres" not in request.keys():
        #    pass
        #else:
            #No tiene nombres.
        #    pass

        nuevo_registro_solicitud["tipo"] = request["tipo"]

        if request["tipo"] == "Propiedad privada":
            nuevo_registro_solicitud["tipo_privada"] = request["tipo_privada"]
            nuevo_registro_solicitud["comprobante_domicilio"] = request["comprobante_domicilio"]
            nuevo_registro_solicitud["comprobante_propiedad"] = request["comprobante_propiedad"]
            if request["tipo_privada"] == "Construcción":
                nuevo_registro_solicitud["construccion"] = {}
                nuevo_registro_solicitud["construccion"]["documento_registro"] = request["documento_registro"]
                nuevo_registro_solicitud["construccion"]["documento_planos"] = request["documento_planos"]
                nuevo_registro_solicitud["construccion"]["comprobante_propiedad"] = request["comprobante_propiedad"]
            elif request["tipo_privada"] == "Riesgo":
                nuevo_registro_solicitud["riesgo"] = {}
                nuevo_registro_solicitud["riesgo"]["documento_dictamen_riesgo"] = request["documento_dictamen_riesgo"]

        return nuevo_registro_ciudadano, nuevo_registro_solicitud

    else:
        #En caso de que no sea un diccionario.
        return None, None
