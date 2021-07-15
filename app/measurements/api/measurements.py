from app import db
from flask import render_template
from app.models import Measurement
from app.measurements import measurement_bp
import json
from flask import request
from app.measurements.constants import PAGE, PER_PAGE
from werkzeug.exceptions import NotFound
from app.measurements.schema import MeasurementResponseSchema, MeasurementPostSchema, MeasurementPutSchema, MeasurementPatchSchema

measurement_response_schema = MeasurementResponseSchema()
measurement_collection_response_schema = MeasurementResponseSchema(many=True)
measurement_post_schema = MeasurementPostSchema()
measurement_collection_post_schema = MeasurementPostSchema(many=True)
measurement_put_schema = MeasurementPutSchema()
measurement_collection_put_schema = MeasurementPutSchema(many=True)
measurement_patch_schema = MeasurementPatchSchema()
measurement_collection_patch_schema = MeasurementPatchSchema(many=True)


@measurement_bp.get('')
def get_all():
    page = int(request.args.get("page", PAGE))
    per_page = int(request.args.get("per_page", PER_PAGE))



    measurements = db.session.query(Measurement).paginate(page=page, per_page=per_page)
    response = {"meta": {"total":measurements.total,
                         "page":measurements.page,
                         "per_page":measurements.per_page},
                "results": []}

    for measurement in measurements.items:
        data = {
            "id": measurement.id,
            "humidity": measurement.humidity,
            "pollution": measurement.pollution,
            "temperature": measurement.temperature
        }
        response['results'].append(data)

    return json.dumps(response)


@measurement_bp.get("/<int:id>")
def get_id(id):
    single = db.session.query(Measurement).filter(Measurement.id == id).first()
    if single:
        return measurement_response_schema.dump(single)
    else:
        return NotFound(
            description='Measurement with {} does not exist'.format(id)
        )


@measurement_bp.get("/latest")
def latest():
    latest = db.session.query(Measurement).order_by(Measurement.id.desc()).first()
    return measurement_response_schema.dump(latest)

@measurement_bp.post("")
def post_measurement():

    data = request.get_json()
    obj = measurement_post_schema.load(data)

    measurement = Measurement(obj.get('temperature'), obj.get('humidity'), obj.get('pollution'))
    db.session.add(measurement)
    db.session.commit()
    # Vracanje klijentu
    data = {
        "id": measurement.id,
        "humidity": measurement.humidity,
        "pollution": measurement.pollution,
        "temperature": measurement.temperature
    }
    return json.dumps(data)


@measurement_bp.put("<int:id>")
def put_measurement(id):

    data = request.get_json()
    obj = measurement_put_schema.load(data)

    measurement = db.session.query(Measurement).filter(Measurement.id == id).first()
    if measurement:
        measurement.temperature = int(obj.get('temperature'))
        measurement.humidity = int(obj.get('humidity'))
        measurement.pollution = int(obj.get('pollution'))
        db.session.commit()
        # Vracanje klijentu
        data = {
            "id": measurement.id,
            "humidity": measurement.humidity,
            "pollution": measurement.pollution,
            "temperature": measurement.temperature
        }
        return json.dumps(data)
    else:
        return NotFound(description=f'There is no measurement with the ID {id}')


@measurement_bp.patch("<int:id>")
def patch_measurement(id):

    data = request.get_json()
    obj = measurement_put_schema.load(data)

    measurement = db.session.query(Measurement).filter(Measurement.id == id).first()
    if measurement.temperature:
        measurement.temperature = int(obj.get('temperature'))
    if measurement.humidity:
        measurement.humidity = int(obj.get('humidity'))
    if measurement.pollution:
        measurement.pollution = int(obj.get('pollution'))
    db.session.commit()
    # Vracanje klijentu
    data = {
        "id": measurement.id,
        "humidity": measurement.humidity,
        "pollution": measurement.pollution,
        "temperature": measurement.temperature
    }
    return json.dumps(data)







