import datetime
import logging
import os

from celery import Celery
from flask import Flask, Response, jsonify, redirect, url_for
import flask_login
from flask_migrate import Migrate

from app import models as m
from app.services.exceptions import InvalidUsage
from app.services.helpers import Helper
from config import Config, config
from flask_ckeditor import CKEditor

def create_app(config_name=None):
    config_name = config_name or (os.getenv('FLASK_CONFIG') or 'development')
    app = Flask(__name__, static_url_path=Config.STATIC_URL_PATH, static_folder=Config.STATIC_FOLDER,
                template_folder=Config.TEMPLATE_FOLDER)
    app.config.from_object(config[config_name])
    if app.config['CONFIG_NAME'] != 'production':
        app.config['APP_VERSION'] = datetime.datetime.timestamp(datetime.datetime.utcnow())

    # logging
    logging_level = app.config.get('LOGGER_LEVEL')
    print('FLASK APP INSTANCE CREATED: create_app({}) - LOG LEVEL: {}'.format(config_name, logging_level))

    # logging_file_handler = logging.FileHandler(Helper.base_path('misc/log/app.log'))
    app.logger.setLevel(logging_level)
    # app.logger.addHandler(logging_file_handler)
    # disable werkzeug verbose access logs
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging_level)
    # disable gunicorn verbose access logs
    gunicorn_logger = logging.getLogger('gunicorn.access')
    gunicorn_logger.setLevel(logging_level)

    # for running db commands in flask app such as: flask db init
    m.db.init_app(app)
    Migrate(app, m.db)

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # Blueprints
    from app import routes as base_routes
    app.register_blueprint(base_routes.bp, url_prefix='')

    # flask_login
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
        
    @login_manager.user_loader
    def user_loader(user_id):
        return m.Users.query.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('base.unauthorized'))
    
    # Editor configs
    ckeditor = CKEditor()
    ckeditor.init_app(app)
    

    # CLI
    from app.cli.tune import cli as tune_cli
    app.cli.add_command(tune_cli)

    if config_name == 'development':
        from app.cli.play import cli as play_cli
        app.cli.add_command(play_cli)

    return app
