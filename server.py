import os
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from app.utils.env import DB, MA
from app.utils.configurations import load_config

# init app
app = Flask(__name__)




with app.app_context():
    # load config
    taxhub_config = load_config()
    app.config.update(taxhub_config)
    
    api = Api(app)

    # Bind app to DB
    DB.init_app(app)
    app.config["DB"] = DB

    # Bind app to MA
    MA.init_app(app)

    from pypnusershub import routes
    app.register_blueprint(routes.routes, url_prefix="/auth")

    from app.core.routes.routestaxref import blp
    api.register_blueprint(blp, url_prefix="/")

    from app.core.routes.routesattributs import blp
    api.register_blueprint(blp, url_prefix="/attributs")


CORS(app, supports_credentials=True)
# Run sever
if __name__ == "__main__":
    app.run(debug=True, port=5052)
