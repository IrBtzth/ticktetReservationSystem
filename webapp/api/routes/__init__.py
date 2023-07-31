from flask_restful import Api


rest_api = Api()


def create_module(app, **kwargs):
    rest_api.add_resource(
        RoutesApi,
        "/api/routes",
        "/api/routes/<int:id>",
    )


    rest_api.init_app(app)