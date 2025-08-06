from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .routes import (
    user_blp, event_blp, seat_blp, ticket_blp, payment_blp, health_blp
)

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["API_TITLE"] = "Event Ticket Booking API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(user_blp)
api.register_blueprint(event_blp)
api.register_blueprint(seat_blp)
api.register_blueprint(ticket_blp)
api.register_blueprint(payment_blp)
