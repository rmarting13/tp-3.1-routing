import json

import requests
from flask import Flask, jsonify, abort, request, url_for
from config import Config
from datetime import date

def init_app():
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    app.config.from_object(Config)

    @app.route('/')  # Ejercicio 1
    def bienvenido():
        return {'message': 'Bienvenidx!'}, 200

    @app.route('/info')  # Ejercicio 2
    def info():
        return {'message': f'Bienvenido a la aplicación {Config.APP_NAME}'}, 200

    @app.get('/about')
    def about():  # Ejercicio 3
        body = {
            'app_name': Config.APP_NAME,
            'description': Config.DESCRIPTION,
            'developers': Config.DEVELOPERS,
            'version': Config.VERSION
        }
        return body, 200

    @app.errorhandler(400)  # Maneja errores producidos por peticiones no válidas (bad requests)
    def argumento_invalido(e):
        return jsonify(error=str(e)), 400

    @app.errorhandler(404)  # Maneja errores de rutas no definidas
    def endpoint_invalido(e):
        return jsonify(error=str(e)), 404

    @app.get('/age/<string:dob>')  # Ejercicio 5
    def calcularEdad(dob):
        try:
            fecha_nac = date.fromisoformat(dob)
            fecha_actual = date.today()
            if fecha_nac < fecha_actual:
                diferencia = (fecha_actual.month, fecha_nac.day) < (fecha_nac.month, fecha_nac.day)  #retorna un boolean
                edad = fecha_actual.year - fecha_nac.year - diferencia  #el valor de diferencia (boolean) es equivalente a 1 (true) ó 0 (false)
                return {'edad': edad}, 200
            else:
                abort(400, description="La fecha ingresada supera a la fecha actual.")
        except ValueError:
            abort(400, description="La fecha ingresada tiene un formato ISO 8601 válido.")

    @app.get('/operate')  # Ejercicio 7
    def operar():
        ops = ['sum', 'sub', 'mult', 'div']
        try:
            op = request.args.get('operation', default='')
            arg1 = request.args.get('num1', default='0')
            arg2 = request.args.get('num2', default='0')
            if op in ops:
                if op == 'sum':
                    result = int(arg1) + int(arg2)
                elif op == 'sub':
                    result = int(arg1) - int(arg2)
                elif op == 'mult':
                    result = int(arg1) * int(arg2)
                else:
                    result = int(arg1) / int(arg2)
                return {'resultado': result}, 200
            else:
                raise ValueError
        except ZeroDivisionError:
            abort(400, description='La división por 0 no está definida.')
        except ValueError:
            abort(404, description='No existe una ruta definida para el endpoint proporcionado.')

    @app.get('/formatted/<string:dni>')  # Ejercicio 9
    def formatear_dni(dni):
        cad = dni.replace('.', '')
        cad = cad.replace('-', '')
        try:
            if len(str(int(cad))) == 8:
                return {'formatted_dni': cad}, 200
            else:
                abort(400, description='-El formato del dni ingresado no es válido.')
        except ValueError:
            abort(400, description='-El dni debe contener sólo caracteres numéricos.')

    @app.get('/encode/<string:keyword>')  # Ejercicio 11
    def encriptar(keyword: str):
        especiales = {'á': 'a', 'ä': 'a', 'é': 'e', 'ë': 'e', 'í': 'i',
                      'ï': 'i', 'ó': 'o', 'ö': 'o', 'ú': 'u', 'ü': 'u'}
        with open('app/static/morse_code.json', 'r') as fo:
            palabras = list(((keyword.strip()).split('+')))
            cad = ''
            morse = json.load(fo)
            for p in palabras:
                if p.isalnum():
                    for l in p:
                        car = especiales.get(l, l)
                        cad = cad + morse.get('letters').get(car.upper()) + '+'
                        if len(cad) == 100:
                            break
                    if len(cad) == 100:
                        break
                    cad += '^+'
                else:
                    abort(400, description='No es posible encriptar caracteres especiales.')
            print(len(cad))
            return {'encoded': cad.strip('+^+')}, 200

    @app.get('/convert/binary/<string:num>')  # Ejercicio 13
    def convertir(num):
        bin = int(num)
        dec = 0
        pos = 0
        while bin > 0:
            bit = bin % 10
            dec += bit*(2**pos)
            bin = int(bin/10)
            pos += 1
        return {'binary_to_decimal': dec}, 200

    return app