from flask import Flask, jsonify


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify({"mesazhi": "Mire se vini ne Qendren e Kujdesit per Kafshe!"})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app