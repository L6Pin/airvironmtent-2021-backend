from flask import  Blueprint

measurement_bp = Blueprint("measurement", __name__, url_prefix="/api/measurements")

import app.measurements.api
