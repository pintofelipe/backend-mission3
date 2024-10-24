from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Namespace para Usuarios
user_ns = Namespace('users', description='Operaciones con usuarios')

# Modelo de entrada para el registro de usuario
user_registration_model = user_ns.model('UserRegistration', {
    'username': fields.String(required=True, description='Nombre de usuario'),
    'email': fields.String(required=True, description='Correo electrónico'),
    'password': fields.String(required=True, description='Contraseña'),
})

# Modelo de entrada para la autenticación de usuario
user_login_model = user_ns.model('UserLogin', {
    'email': fields.String(required=True, description='Correo electrónico'),
    'password': fields.String(required=True, description='Contraseña'),
})

# Modelo de salida para el usuario
user_response_model = user_ns.model('UserResponse', {
    'id': fields.Integer(description='ID del usuario'),
    'username': fields.String(description='Nombre de usuario'),
    'email': fields.String(description='Correo electrónico del usuario'),
})

# Modelo para el token de acceso
token_response_model = user_ns.model('TokenResponse', {
    'access_token': fields.String(description='Token de acceso JWT')
})

# **Registro y Autenticación de Usuarios**
@user_ns.route('/register')
class UserRegisterResource(Resource):
    @user_ns.expect(user_registration_model, validate=True)
    @user_ns.marshal_with(user_response_model, code=201)
    def post(self):
        """Registrar un nuevo usuario"""
        data = request.get_json()
        try:
            user = UserService.create_user(data['username'], data['email'], data['password'])
            return user, 201
        except ValueError as e:
            user_ns.abort(400, str(e))

@user_ns.route('/login')
class UserLoginResource(Resource):
    @user_ns.expect(user_login_model, validate=True)
    @user_ns.marshal_with(token_response_model)
    def post(self):
        """Autenticar un usuario y obtener un token de acceso"""
        data = request.get_json()
        try:
            user = UserService.authenticate_user(data['email'], data['password'])
            # Si la autenticación es correcta, crear un token JWT
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        except ValueError as e:
            user_ns.abort(401, str(e))

# **Operaciones en Usuario Específico**
@user_ns.route('/<int:user_id>')
@user_ns.param('user_id', 'El identificador único del usuario')
class UserResource(Resource):
    @jwt_required()
    @user_ns.marshal_with(user_response_model)
    def get(self, user_id):
        """Obtener un usuario por ID"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            user_ns.abort(404, 'User not found')
        return user, 200

    @jwt_required()
    @user_ns.expect(user_registration_model, validate=True)
    @user_ns.marshal_with(user_response_model)
    def put(self, user_id):
        """Actualizar un usuario existente"""
        data = request.get_json()
        try:
            user = UserService.update_user(user_id, data['username'], data['email'], data['password'])
            return user, 200
        except ValueError as e:
            user_ns.abort(400, str(e))

    @jwt_required()
    def delete(self, user_id):
        """Eliminar un usuario por ID"""
        try:
            UserService.delete_user(user_id)
            return {'message': 'User deleted successfully'}, 204
        except ValueError as e:
            user_ns.abort(404, str(e))

# **Perfil del Usuario Actual**
@user_ns.route('/me')
class UserProfileResource(Resource):
    @jwt_required()
    @user_ns.marshal_with(user_response_model)
    def get(self):
        """Obtener información del usuario actual"""
        user_id = get_jwt_identity()
        user = UserService.get_user_by_id(user_id)
        if not user:
            user_ns.abort(404, 'User not found')
        return user, 200
