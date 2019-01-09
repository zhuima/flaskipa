import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from flaskipa.blueprints.auth import auth_bp
from flaskipa.extensions import bootstrap, db, login_manager, csrf,  moment
from flaskipa.models import User
from flaskipa.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('flaskipa')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_errors(app)
    return app


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/flaskipa.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)


    if not app.debug:
        app.logger.addHandler(file_handler)


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400
