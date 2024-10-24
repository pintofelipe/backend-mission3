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
    status = db.Column(db.String(50), nullable=False, default='pending') # Estdo de la tarea (Pending, completed)
    due_date = db.Column(db.DateTime, nullable=True) # Fecha limite para completar la tarea
    create_at = db.Column(db.DateTime, ) # Fecha de creacion de la tarea




    # Relación muchos a muchos con categorías usando la tabla intermedia 'task_category'
    categories = db.relationship('Category', 
                                 secondary=task_category,  # Tabla intermedia que define la relación
                                 backref=db.backref('tasks', lazy='dynamic'))  # Permite acceso inverso desde categorías a tareas

    def __init__(self, title, description=None, completed=False):
        """
        Constructor de la clase Task.

        Args:
            title (str): El título de la tarea.
            description (str, opcional): La descripción de la tarea.
            completed (bool, opcional): Indica si la tarea está completada o no, por defecto es False.
        """
        self.title = title
        self.description = description
        self.completed = completed
