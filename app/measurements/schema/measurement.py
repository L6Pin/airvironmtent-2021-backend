from marshmallow import Schema, fields, validate, pre_load, ValidationError
from app.measurements.constants import PAGE, PER_PAGE


class MeasurementResponseSchema(Schema):
    id = fields.Integer(required=False)
    temperature = fields.Float()
    pollution = fields.Float()
    humidity = fields.Float()
    created = fields.DateTime()


class MeasurementPostSchema(Schema):
    temperature = fields.Float(validate=validate.Range(-20, 65), required=True)
    pollution = fields.Float(validate=validate.Range(0, 500), required=True)
    humidity = fields.Float(validate=validate.Range(0, 100), required=True)


class MeasurementPutSchema(Schema):
    temperature = fields.Float(validate=validate.Range(-20, 65), required=True)
    pollution = fields.Float(validate=validate.Range(0, 500), required=True)
    humidity = fields.Float(validate=validate.Range(0, 100), required=True)


class MeasurementPatchSchema(Schema):
    temperature = fields.Float(validate=validate.Range(-20, 65))
    pollution = fields.Float(validate=validate.Range(0, 500))
    humidity = fields.Float(validate=validate.Range(0, 100))

    @pre_load()
    def test(self, data):
        if 'temperature' not in data and 'pollution' \
                not in data and 'humidity' not in data:
            raise ValidationError('Patch body should have at least '
                                  'one param')

    class MeasurementMetaSchema(Schema):
        page = fields.Integer(default=5)
        per_page = fields.Integer(missing=5)
        total = fields.Integer(misisng=0)

        @pre_load()
        def load(self, data, **kwargs):
            if 'per_page' not in data:
                data['per_page'] = 5
            return data

class MeasurementMetaSchema(Schema):
    page = fields.Integer(required=False, default=PAGE, missing=PAGE)
    per_page = fields.Integer(required=False, default=PER_PAGE, missing=PER_PAGE)
    total = fields.Integer(required=False, missing=0, default=0)

class MeasurementPaginationSchema(Schema):
    meta = fields.Method('get_meta')
    results = fields.Method('get_results')

    @staticmethod
    def get_meta(data):
        response = dict()
        response["total"] = data.total
        response["page"] = data.page
        response["per_page"] = data.per_page
        return MeasurementMetaSchema().dump(response)

    @staticmethod
    def get_results(data):
        return MeasurementResponseSchema(many=True).dump(data.items)