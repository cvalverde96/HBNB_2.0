#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')


review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        current_user = get_jwt_identity()
        review_data = api.payload
        
        review_data['user_id'] = current_user
        try:
            place = facade.get_place(review_data['place_id'])
            if place['owner_id'] == current_user:
                return {'error': 'You cannot review your own place'}, 400
            
            existing_review = facade.get_review_by_user_and_place(current_user, review_data['place_id'])
            if existing_review:
                return {'error': 'You have already reviewed this place.'}, 400

            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        reviews = facade.get_all_reviews()
        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user': {
                'id': r.user.id,
                'first_name': r.user.first_name,
                'last_name': r.user.last_name
            },
            'place': {
                'id': r.place.id,
                'title': r.place.title
            }
        } for r in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        try:
            review = facade.get_review(review_id)
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name
                },
                'place': {
                    'id': review.place.id,
                    'title': review.place.title
                }
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        current_user = get_jwt_identity()
        review_data = api.payload
        
        try:
            review = facade.get_review(review_id)
            
            if review.user.id != current_user:
                return {'error': 'Unauthorized action'}, 403
            
            updated_review = facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        current_user = get_jwt_identity()
        
        try:
            review = facade.get_review(review_id)
            if review.user.id != current_user:
                return {'error': 'Unauthorized action'}, 403
            
            message = facade.delete_review(review_id)
            return {'message': message}, 200
        except ValueError as e:
            return {'error': str(e)}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [{
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user': {
                    'id': r.user.id,
                    'first_name': r.user.first_name,
                    'last_name': r.user.last_name
                }
            } for r in reviews], 200
        except ValueError as e:
            return {'error': str(e)}, 404