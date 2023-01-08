from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = "asdsad"

    from . import url_short
    app.register_blueprint(url_short.bp)

    return app
