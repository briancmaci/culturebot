from aquabot import create_app, config
from aquabot.models import db, User


app = create_app(config.DevelopmentConfig)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

