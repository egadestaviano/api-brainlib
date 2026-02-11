import os
import importlib
import pkgutil
from flask import Flask, jsonify
from flask_cors import CORS


from app.config import init_database_from_env

try:
    from flasgger import Swagger
except Exception:
    Swagger = None


def register_blueprints(app: Flask, package_name: str, package_path: str, url_prefix: str = "/api") -> None:
    """Dynamically find and register all Blueprints in a package."""
    for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
        if is_pkg:
            continue
        module_full = f"{package_name}.{module_name}"
        module = importlib.import_module(module_full)

        for attr in dir(module):
            obj = getattr(module, attr)
            if getattr(obj, "register", None) and getattr(obj, "name", None):
                prefix = url_prefix + (obj.url_prefix or "")
                app.register_blueprint(obj, url_prefix=prefix)
                print(f"route: {prefix}")


def create_app() -> Flask:
    init_database_from_env()
    app = Flask(__name__)
    
    cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": cors_origins}})


    @app.get("/")
    def index():
        return jsonify({"status": "error", "code": 401})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    routes_path = os.path.join(os.path.dirname(__file__), "routes")
    register_blueprints(app, "app.routes", routes_path, url_prefix="/api")

    if Swagger is not None:
        template = {
            "swagger": "2.0",
            "info": {"title": "LMS Backend API", "version": "1.0.0"},
            "basePath": "/api",
            "schemes": ["http"],
        }
        config = {
            "headers": [],
            "specs": [
                {
                    "endpoint": "apispec_1",
                    "route": "/api/apispec_1.json",
                    "rule_filter": lambda rule: True,
                    "model_filter": lambda tag: True,
                }
            ],
            "static_url_path": "/flasgger_static",
            "swagger_ui": True,
            "specs_route": "/api/",
        }
        Swagger(app, template=template, config=config)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "1") == "1",
    )
