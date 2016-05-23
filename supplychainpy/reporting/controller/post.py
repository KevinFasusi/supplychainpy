from flask.ext.restful import Api
from flask.ext.restful import Resource

rest_api = Api()


class TestApi(Resource):
    def get(self):
        return {'hello':'world'}
