from datetime import datetime
import json
import os
import re


def validar_curp(curp: str):
    regex = r"^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$"

    is_curp_valid = re.match(regex, curp)

    if is_curp_valid:
        return True
    return False


def validar_rfc(rfc: str):
    regex = r"^([A-ZÑ&]{3,4}) ?(?:- ?)?(\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])) ?(?:- ?)?([A-Z\d]{2})([A\d])$"

    is_rfc_valid = re.match(regex, rfc)

    if is_rfc_valid:
        return True
    return False


def validar_cp(cp: int):
    if not len(str(cp)) == 5:
        return False
    if int(str(cp)[:2]) == 00:
        return False
    return True


def validar_fecha(fecha: str):
    try:
        datetime.strptime(fecha, '%d-%m-%Y')
        return True
    except ValueError:
        return False


def validar_telefono(telefono: int):
    if not len(str(telefono)) == 10:
        return False
    return True


def validar_estado(estado: str):
    estados_json = open("utils/estados.json")
    estados_data = json.load(estados_json)

    estado_valid = False
    for element in estados_data:
        if element["nombre"] == estado.upper():
            estado_valid = True
            break

    return estado_valid


def validar_municipio(estado: str, municipio: str):
    municipios_json = open("utils/estados_municipios.json")
    municipios_data = json.load(municipios_json)

    municipios_estado = {
        el.lower(): True for el in municipios_data[estado.upper()]}
    if municipio.lower() in municipios_estado:
        return True
    else:
        return False
