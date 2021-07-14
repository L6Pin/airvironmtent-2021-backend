from app import db
from flask import render_template
from app.models import Measurement
from app.measurements import measurement_bp
import json
from flask import request
from app.measurements.constants import PAGE, PER_PAGE
from werkzeug.exceptions import NotFound

@measurement_bp.get('')
def get_all():
    page = int(request.args.get("page", PAGE))
    per_page = int(request.args.get("per_page", PER_PAGE))

    measurements = db.session.query(Measurement).paginate(page=page, per_page=per_page)
    response = {"meta":{"total":measurements.total,
                        "page":measurements.page,
                        "per_page":measurements.per_page},
                        "results":[]}

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
        data = {
            "id": single.id,
            "humidity": single.humidity,
            "pollution": single.pollution,
            "temperature": single.temperature
        }
        return json.dumps(data)
    else:
        return NotFound(
            description='Measurement with {} does not exist'.format(id)
        )


@measurement_bp.get("/latest")
def latest():
    latest = db.session.query(Measurement).order_by(Measurement.id.desc()).first()
    if latest:
        data = {
            "id": latest.id,
            "humidity": latest.humidity,
            "pollution": latest.pollution,
            "temperature": latest.temperature
        }
        return json.dumps(data)
    else:
        return NotFound()


@measurement_bp.post("")
def post_measurement():
    data = request.get_json()
    temp = data.get('temperature')
    hum = data.get('humidity')
    pol = data.get('pollution')

    if temp and hum and pol:
        measurement = Measurement(temp, hum, pol)
        db.session.add(measurement)
        db.session.commit()
        data = {
            "id": measurement.id,
            "humidity": measurement.humidity,
            "pollution": measurement.pollution,
            "temperature": measurement.temperature
        }
        return json.dumps(data)
    else:
        return NotFound()


@measurement_bp.put("<int:id>")
def put_measurement(id):
    import pdb; pdb.set_trace()
    data = request.get_json()
    temp = data.get('temperature')
    hum = data.get('humidity')
    pol = data.get('pollution')

    if temp and hum and pol:
        measurement = db.session.query(Measurement).filter(Measurement.id == id).first()
        if measurement:
            measurement.temperature=int(temp)
            measurement.humidity=int(hum)
            measurement.pollution=int(pol)
            db.session.commit()
            data = {
                "id": measurement.id,
                "humidity": measurement.humidity,
                "pollution": measurement.pollution,
                "temperature": measurement.temperature
            }
            return json.dumps(data)
        else:
            return NotFound(description=f'There is no measurement with the ID {id}')
    else:
        return NotFound()







    # all = request.args.get('all')
    # if all:
    #     return {"asdf": 1}
    # klimaInfo = db.session.query(Measurement).all()
    # list_of_measurements = []
    #
    # for measurement in klimaInfo:
    #     data = {
    #         "id": measurement.id,
    #         "humidity": measurement.humidity,
    #         "pollution": measurement.pollution,
    #         "temperature": measurement.temperature
    #     }
    #     list_of_measurements.append(data)
    #     return json.dumps(list_of_measurements)


# @app.route("/1")
# def hello_world():
#     klimaInfo = db.session.query(Measurement).all()
#     return render_template("home.html", klimaInfo=klimaInfo)


