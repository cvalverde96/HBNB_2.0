#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity succesfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return ({'id': new_amenity.id, 'name': new_amenity.name}, 201)
        except ValueError as e:
            return ({'error': str(e)}, 400)
    @api.response(200, 'List of amenities retrieved succesfully')
    def get(self):
        amenities = facade.get_all_amenities()
        return ([{'id': a.id, 'name': a.name} for a in amenities], 200)

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved succesfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        try:
            amenity = facade.get_amenity(amenity_id)
            return ({'id': amenity.id, 'name': amenity.name}, 200)
        except ValueError as e:
            return ({'error': str(e)}, 404)
    @api.expect(amenity_model)
    @api.response(200,'Amenity updated succesfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        amenity_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return ({'id': updated_amenity.id, 'name': updated_amenity.name}, 200)
        except ValueError as e:
            return ({'error': str(e)}, 400)