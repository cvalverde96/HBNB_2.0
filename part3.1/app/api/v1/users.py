#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
import uuid

api = Namespace('users', description='User operations')


user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'is_admin': fields.Boolean(required=True, description='User is admin'),
    'password': fields.String(required=True, description='Password for the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
    
        try:
            new_user = facade.create_user({
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'password': user_data['password'],
                'is_admin': user_data['is_admin']
            })

        except ValueError as e:
            return {'error': str(e)}, 400
        
        return {
            'id': new_user.id, 
            'first_name': new_user.first_name, 
            'last_name': new_user.last_name, 
            'email': new_user.email,
            'is_admin': new_user.is_admin
            }, 201
    
    @api.response(200, 'User list retrieved succesfully')
    def get(self):
        users = facade.get_all_users()
        user_list = [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'password': user.password} for user in users]
        return user_list, 200
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
    
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User information updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        current_user = get_jwt_identity()
        user_data = api.payload
        
        try:
            user_id = str(uuid.UUID(user_id))
        except ValueError:
            return {'error': 'Invalid user ID format'}, 400
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        if user_id != current_user:
            return {'error': 'Unauthorized action (users.py)'}, 403
        
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password.'}, 400
        
        updated_user = facade.update_user(user_id, user_data)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200