#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('placeamenities', description='Place Amenity Operations')

place_amenity_model = api.model('PlaceAmenity', {
    'place_id': fields.String(required=True, description='ID of the place', example='123'),
    'amenity_id': fields.String(required=True, description='ID of the amenity', example='456'),
})


@api.route('/')
class PlaceAmenities(Resource):
    def get(self):
        try:
            place_amenities = facade.get_place_amenity()

            place_amenity_data = [
                {
                    'place_id': pa.place_id,
                    'amenity_id': pa.amenity_id
                } for pa in place_amenities
            ]
            return place_amenity_data, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.expect(place_amenity_model)
    def post(self):
        current_user = get_jwt_identity()
        print("Current user identity:", current_user)

        place_amenity_data = api.payload
        if not place_amenity_data:
            return {'error': 'Invalid or missing JSON payload'}, 400

        if 'place_id' not in place_amenity_data or 'amenity_id' not in place_amenity_data:
            return {'error': 'place_id and amenity_id are required'}, 400

        place = facade.get_place(place_amenity_data['place_id'])
        if not place:
            return {'error': 'Place Not Found'}, 404

        amenity = facade.get_amenity(place_amenity_data['amenity_id'])
        if not amenity:
            return {'error': 'Amenity Not Found'}, 404

        user = facade.get_user(current_user['id'])
        if not user:
            return {'error': 'User Not Found'}, 404

        try:
            new_place_amenity = facade.create_place_amenity(place_amenity_data)

            created_place_amenity_data = {
                'place_id': new_place_amenity.place_id,
                'amenity_id': new_place_amenity.amenity_id
            }

            return created_place_amenity_data, 201
        except Exception as e:
            return {'error': str(e)}, 400
