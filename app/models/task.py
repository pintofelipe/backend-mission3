from datetime import datetime  # Import necesario para la fecha
from app import db

# Tabla intermedia para la relación de muchos a muchos entre Tareas y Categorías
task_category = db.Table('task_category',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),  # Referencia a la tabla 'tasks'
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)  # Referencia a la tabla 'categories'
)

class Task(db.Model):
    __tablename__ = 'tasks'  # Nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    title = db.Column(db.String(120), nullable=False)  # Título de la tarea, no puede ser nulo
    description = db.Column(db.String(255), nullable=True)  # Descripción de la tarea, es opcional
    status = db.Column(db.String(50), nullable=False, default='pending')  # Estado de la tarea (pending, completed)
    due_date = db.Column(db.DateTime, nullable=True)  # Fecha límite para completar la tarea
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de creación de la tarea
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ID del usuario que creó la tarea

    # Relación muchos a muchos con categorías usando la tabla intermedia 'task_category'
    categories = db.relationship('Category', 
                                 secondary=task_category,  # Tabla intermedia que define la relación
                                 backref=db.backref('tasks', lazy='dynamic'))  # Permite acceso inverso desde categorías a tareas

    def __init__(self, title, description=None, status='pending', due_date=None, user_id=None):
        """
        Constructor de la clase Task.

        Args:
            title (str): El título de la tarea.
            description (str, opcional): La descripción de la tarea.
            status (str, opcional): El estado de la tarea, por defecto es 'pending'.
            due_date (datetime, opcional): La fecha límite para completar la tarea.
            user_id (int, opcional): ID del usuario que creó la tarea.
        """
        self.title = title
        self.description = description
        self.status = status
        self.due_date = due_date
        self.user_id = user_id
