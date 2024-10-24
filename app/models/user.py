from datetime import datetime
from app import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'  # Nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nombre de usuario único
    email = db.Column(db.String(120), unique=True, nullable=False)  # Correo electrónico único
    password_hash = db.Column(db.String(128), nullable=False)  # Contraseña hasheada
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de creación del usuario

    # Relación uno a muchos: Un usuario puede tener muchas tareas
    tasks = db.relationship('Task', backref='user', lazy=True)  # Relación con la tabla 'tasks'

    def __init__(self, username, email, password):
        """
        Constructor de la clase User.

        Args:
            username (str): Nombre del usuario.
            email (str): Correo electrónico del usuario.
            password (str): Contraseña en texto plano que se hasheará antes de guardarla.
        """
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con la hasheada.

        Args:
            password (str): Contraseña en texto plano a verificar.

        Returns:
            bool: True si la contraseña es correcta, False en caso contrario.
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Representación en formato string del objeto User.

        Returns:
            str: Representación del usuario.
        """
        return f'<User {self.username}>'
