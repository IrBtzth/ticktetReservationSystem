import datetime

from flask import abort, current_app, jsonify, request
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from webapp.app.models import db, Routes

from .parsers import (
    route_get_parser,
    route_route_parser,
    route_put_parser,
)
from .fields import HTMLField



routes_fields = {
    'id': fields.Integer(),
    'from': fields.String(),
    'to': fields.String()
}


class RoutesApi(Resource):
    @marshal_with(route_fields)
    @jwt_required
    def get(self, route_id=None):
        if routes_id:
            route = Routes.query.get(route_id)
            if not route:
                abort(404)
            return route
        else:
            args = route_get_parser.parse_args()
            page = args['page'] or 1

            if args['user']:
                user = User.query.filter_by(username=args['user']).first()
                if not user:
                    abort(404)

                routes = user.routes.order_by(
                    Post.publish_date.desc()
                ).paginate(page, current_app.config['POSTS_PER_PAGE'])
            else:
                routes = Post.query.order_by(
                    Post.publish_date.desc()
                ).paginate(page, current_app.config['POSTS_PER_PAGE'])

            return routes.items

    @jwt_required
    def route(self):
        print(request.data)
        args = route_route_parser.parse_args(strict=True)
        new_route = Post(args['from'])
        new_route.user_id = get_jwt_identity()
        new_route.to = args['to']

        db.session.add(new_route)
        db.session.commit()
        return {'id': new_route.id}, 201

    @jwt_required
    def put(self, route_id=None):
        if not route_id:
            abort(400)
        route = Routes.query.get(route_id)
        if not route:
            abort(404)
        args = route_put_parser.parse_args(strict=True)
        if get_jwt_identity() != route.user_id:
            abort(403)
        if args['from']:
            route.title = args['from']
        if args['to']:
            route.to = args['to']
    

        db.session.merge(route)
        db.session.commit()
        return {'id': route.id}, 201

    @jwt_required
    def delete(self, route_id=None):
        if not route_id:
            abort(400)
        route = Routes.query.get(route_id)
        if not route:
            abort(404)
        if get_jwt_identity() != route.user_id:
            abort(401)

        db.session.delete(route)
        db.session.commit()
        return "", 204