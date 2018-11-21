import os
from flask import Flask, cli
from explorer.models import db
from explorer import models, routes, scripts
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    cli.load_dotenv()
    app.config.from_object(os.environ['APP_SETTINGS'])
    # Init app
    db.init_app(app)
    routes.init_app(app)
    scripts.init_app(app)
    # Migarate
    Migrate(app, db)
    return app


app = create_app()

@app.shell_context_processor
def make_shell_context():
    ctx = {
        'db':db,
        'Report':models.Report,
        'Disease':models.Disease,
        's':db.session,
    }
    return ctx


