from flask import Flask
from aquabot.admin import admin
from aquabot.api import api
from aquabot.slackbot import slackbot
from aquabot.models import db, migrate, login


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize database
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        login.init_app(app)

    login.login_view = 'admin.login'

    # Register blueprints
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(slackbot, url_prefix='/slackbot')

    return app
