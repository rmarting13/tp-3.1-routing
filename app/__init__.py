import requests
from flask import Flask, jsonify, abort, request
from config import Config
from datetime import date
def init_app():
    """Crea y configura la aplicación Flask"""
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
            abort(400, description='No existe una ruta definida para el endpoint proporcionado.')

    return app
