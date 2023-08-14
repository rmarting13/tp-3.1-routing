#import requests
from flask import Flask, redirect, request, jsonify
from config import Config
def init_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    app.config.from_object(Config)

    @app.route('/')
    def bienvenido():
        return {'message': 'Bienvenidx!'}, 200

    @app.route('/info')
    def info():
        return {'message': f'Bienvenido a la aplicación {Config.APP_NAME}'}, 200

    @app.get('/about')
    def about():
        body = {
            'app_name': Config.APP_NAME,
            'description': Config.DESCRIPTION,
            'developers': Config.DEVELOPERS,
            'version': Config.VERSION
        }
        return body, 200

    return app
