import os
import click
from flask import Flask
from werkzeug.security import generate_password_hash

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "webapp.sqlite"),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        print("instance path: ", app.instance_path)
    except OSError:
        pass

    from . import db
    from . import auth
    from . import internal

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(internal.bp)
    app.add_url_rule('/', endpoint='auth.login')

    @app.cli.command("add-admin")
    @click.argument("passkey")
    @click.option("--notes")
    def add_admin(passkey, notes):
        database = db.get_db()
        try:
            database.execute(
                "INSERT INTO passkeys (passkey, used, admin, notes) VALUES (?, ?, ?, ?)",
                (generate_password_hash(passkey), 0, 1, notes),
            )
            database.commit()
        except database.IntegrityError:
            raise ValueError(f"Passkey {passkey} is already registered.")
        print(f"Success! Added {passkey} as admin, with notes: {notes}")

    return app
