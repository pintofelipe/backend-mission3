from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    """Servicio para manejar las operaciones CRUD y lógicas de los usuarios."""

    @staticmethod
    def create_user(username, email, password):
        """Crear un nuevo usuario.
        
        Args:
            username (str): Nombre de usuario.
            email (str): Dirección de correo electrónico.
            password (str): Contraseña del usuario.

        Returns:
            User: El nuevo usuario creado.

        Raises:
            ValueError: Si el usuario o el correo electrónico ya existen.
        """
        # Comprobar si el usuario o el email ya existen en la base de datos
        if User.query.filter_by(username=username).first():
            raise ValueError('Username already exists')
        if User.query.filter_by(email=email).first():
            raise ValueError('Email already exists')
        
        # Crear un nuevo usuario con la contraseña encriptada
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        # Agregar el nuevo usuario a la sesión de base de datos
        db.session.add(new_user)
        
        # Confirmar los cambios y guardar el nuevo usuario en la base de datos
        db.session.commit()
        
        return new_user

    @staticmethod
    def get_user_by_id(user_id):
        """Obtener un usuario por su ID.
        
        Args:
            user_id (int): El ID del usuario a buscar.

        Returns:
            User: El usuario encontrado.

        Raises:
            ValueError: Si el usuario no se encuentra.
        """
        # Buscar el usuario por su ID
        user = User.query.get(user_id)
        
        # Si no se encuentra el usuario, lanzar un error
        if not user:
            raise ValueError('User not found')
        
        return user

    @staticmethod
    def get_user_by_username(username):
        """Obtener un usuario por su nombre de usuario.
        
        Args:
            username (str): Nombre de usuario a buscar.

        Returns:
            User: El usuario encontrado.

        Raises:
            ValueError: Si el usuario no se encuentra.
        """
        # Buscar el usuario por su nombre de usuario
        user = User.query.filter_by(username=username).first()
        
        # Si no se encuentra el usuario, lanzar un error
        if not user:
            raise ValueError('User not found')
        
        return user

    @staticmethod
    def update_user(user_id, username=None, email=None, password=None):
        """Actualizar la información de un usuario existente.
        
        Args:
            user_id (int): El ID del usuario a actualizar.
            username (str, opcional): Nuevo nombre de usuario.
            email (str, opcional): Nuevo correo electrónico.
            password (str, opcional): Nueva contraseña.

        Returns:
            User: El usuario actualizado.

        Raises:
            ValueError: Si el usuario no se encuentra o si el nombre de usuario/correo ya existen.
        """
        # Buscar el usuario por su ID
        user = User.query.get(user_id)
        
        # Si el usuario no existe, lanzar un error
        if not user:
            raise ValueError('User not found')
        
        # Verificar si el nuevo nombre de usuario ya existe
        if username and username != user.username and User.query.filter_by(username=username).first():
            raise ValueError('Username already exists')
        
        # Verificar si el nuevo correo ya existe
        if email and email != user.email and User.query.filter_by(email=email).first():
            raise ValueError('Email already exists')
        
        # Si se proporciona un nuevo nombre de usuario, actualizarlo
        if username:
            user.username = username
        
        # Si se proporciona un nuevo correo, actualizarlo
        if email:
            user.email = email
        
        # Si se proporciona una nueva contraseña, actualizarla
        if password:
            user.password_hash = generate_password_hash(password)
        
        # Confirmar los cambios y actualizar el usuario en la base de datos
        db.session.commit()
        
        return user

    @staticmethod
    def delete_user(user_id):
        """Eliminar un usuario existente.
        
        Args:
            user_id (int): El ID del usuario a eliminar.

        Raises:
            ValueError: Si el usuario no se encuentra.
        """
        # Buscar el usuario por su ID
        user = User.query.get(user_id)
        
        # Si el usuario no existe, lanzar un error
        if not user:
            raise ValueError('User not found')
        
        # Eliminar el usuario de la base de datos
        db.session.delete(user)
        
        # Confirmar los cambios
        db.session.commit()

    @staticmethod
    def authenticate_user(username, password):
        """Autenticar un usuario con su nombre de usuario y contraseña.
        
        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña proporcionada para la autenticación.

        Returns:
            User: El usuario autenticado si las credenciales son correctas.

        Raises:
            ValueError: Si el usuario no se encuentra o la contraseña es incorrecta.
        """
        # Buscar el usuario por su nombre de usuario
        user = User.query.filter_by(username=username).first()
        
        # Si el usuario no se encuentra o la contraseña es incorrecta, lanzar un error
        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError('Invalid username or password')
        
        return user

    @staticmethod
    def get_all_users():
        """Obtener todos los usuarios existentes.
        
        Returns:
            List[User]: Lista de todos los usuarios en la base de datos.
        """
        # Devolver todos los usuarios almacenados
        return User.query.all()
