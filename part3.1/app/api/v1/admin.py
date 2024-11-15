from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request
from app.services import facade

api = Namespace('admin', description='Admin operations')

@api.route('/users/<user_id>')
class AdminUserResource(Resource):
  @jwt_required()
  def put(self, user_id):
    jwt_payload = get_jwt()
    print("JWT Payload:", jwt_payload)
    if jwt_payload.get('sub', {}).get('is_admin') is not True:
      return {'error': 'Admin privileges required'}, 403
    
  
    data = request.json
    email = data.get('email')
    
    if email:
      existing_user = facade.get_user_by_email(email)
      if existing_user and existing_user.id != user_id:
        return {'error': 'Email is already in use'}, 400
      
    updated_user = facade.update_user(user_id, data)
    if not updated_user:
      return {'error': 'User not found'}, 404
    
    return {
      'message': 'User updated successfully',
      'user': {
        'id': updated_user.id,
        'email': updated_user.email,
        'first_name': updated_user.first_name,
        'last_name': updated_user.last_name
      }
    }, 200

@api.route('/users/')
class AdminUserCreate(Resource):
  @jwt_required()
  def post(self):
    jwt_payload = get_jwt()
    print("JWT Payload:", jwt_payload)
    if jwt_payload.get('sub', {}).get('is_admin') is not True:
      return {'error': 'Admin privileges required'}, 403
    
    
    user_data = request.json
    email = user_data.get('email')
    
    if facade.get_user_by_email(email):
      return {'error': 'Email already registered'}, 400
    
    is_admin = user_data.get("is_admin", False)
    
    new_user = facade.create_user(
      first_name=user_data["first_name"],
      last_name=user_data["last_name"],
      email=user_data["email"],
      password=user_data["password"],
      is_admin=is_admin  # Pass the is_admin value here
    )
    
    return {
      'message': 'User created succesfully',
      'user': {
        'id': new_user.id,
        'email': new_user.email,
        'first_name': new_user.first_name,
        'last_name': new_user.last_name
      }
    }, 201
    
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
  @jwt_required()
  def post(self):
    jwt_payload = get_jwt()
    print("JWT Payload:", jwt_payload)
    if jwt_payload.get('sub', {}).get('is_admin') is not True:
      return {'error': 'Admin privileges required'}, 403
    
    
    amenity_data = request.json
    name = amenity_data.get('name')
    
    if not name:
      return {'error': 'Amenity name is required'}, 400
  
    try:
      new_amenity = facade.create_amenity(amenity_data)
      return {
        'message': 'Amenity created successfully',
        'amenity': {
          'id': new_amenity.id,
          'name': new_amenity.name
          }
        }, 201
    except ValueError as e:
      return {'error': str(e)}, 400
    
@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
  @jwt_required()
  def put(self, amenity_id):
    jwt_payload = get_jwt()
    print("JWT Payload:", jwt_payload)
    if jwt_payload.get('sub', {}).get('is_admin') is not True:
      return {'error': 'Admin privileges required'}, 403
    
    
    amenity_data = request.json
    name = amenity_data.get('name')
    
    if not name:
      return {'error': 'Amenity name is required'}, 400
    
    try:
      updated_amenity = facade.update_amenity(amenity_id, amenity_data)
      if not updated_amenity:
        return {'error': 'Amenity not found'}, 404
      
      return {
        'message': 'Amenity updated successfully',
        'amenity': {
          'id': updated_amenity.id,
          'name': updated_amenity.name
        }
      }, 200
    except ValueError as e:
      return {'error': str(e)}, 400
    
@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
  @jwt_required()
  def put(self, place_id):
    jwt_payload = get_jwt()
    print("JWT Payload:", jwt_payload)
    if jwt_payload.get('sub', {}).get('is_admin') is not True:
      return {'error': 'Admin privileges required'}, 403
    
    is_admin = jwt_payload.get('is_admin', False)
    user_id = jwt_payload.get('id')
    
    place = facade.get_place(place_id)
    if not is_admin and place.owner_id != user_id:
      return {'error': 'Unauthorized action(admin.py)'}, 403
    
    update_data = request.json
    
    try:
      updated_place = facade.update_place(place_id, update_data)
      if not updated_place:
        return {'error': 'Place not found'}, 404
      
      return {
        'message': 'Place updated successfully',
        'place': {
          'id': updated_place.id,
          'title': updated_place.title,
          'description': updated_place.description,
          'price': updated_place.price,
          'latitude': updated_place.latitude,
          'longitude': updated_place.longitude,
          'owner_id': updated_place.owner.id
        }
      }, 200
    except ValueError as e:
      return {'error': str(e)}, 400