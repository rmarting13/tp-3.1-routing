#import requests
from flask import Flask, redirect, request
from config import Config
def init_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    app.config.from_object(Config)

    @app.route('/')
    def bienvenido():
        return 'Bienvenidx!'

    @app.route('/info')
    def info():
        return 'Bienvenido a la aplicacion' + Config.APP_NAME


    return app
