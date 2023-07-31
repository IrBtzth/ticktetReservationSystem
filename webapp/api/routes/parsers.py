from flask_restful import reqparse

route_get_parser = reqparse.RequestParser()
route_get_parser.add_argument('page', type=int, location=['args', 'headers'])

route_route_parser = reqparse.RequestParser()
route_route_parser.add_argument(
    'title',
    type=str,
    required=True,
    help="From text is required",
    location=('json', 'values')
)
route_route_parser.add_argument(
    'text',
    type=str,
    required=True,
    help="To text is required",
    location=('json', 'values')
)