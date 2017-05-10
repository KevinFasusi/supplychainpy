from flask_restful import Api
from flask_restful import Resource

rest_api = Api()


class TestApi(Resource):
    def get(self):
        return {'hello':'world'}
