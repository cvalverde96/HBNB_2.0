from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
  'email': fields.String(required=True, description='User email'),
  'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
  @api.expect(login_model)
  def post(self):
    credentials = api.payload
    
    user = facade.get_user_by_email(credentials['email'])
    
    if not user or not user.verify_password(credentials['password']):
      return {'error': 'Invalid credentials'}, 401
    
    print(f"is_admin for user {user.id}: {user.is_admin}")

    access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
    
    return {'access_token': access_token}, 200
  
@api.route('/protected')
class ProtectedResource(Resource):
  @jwt_required()
  def get(self):
    current_user_id = get_jwt_identity()
    return {'message': f'Hello, user {current_user_id}'}, 200
  