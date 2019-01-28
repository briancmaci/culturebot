from culturebot import create_app, config
from culturebot.models import db, User


app = create_app(config.DevelopmentConfig)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == '__main__':
    app.run(debug=True)