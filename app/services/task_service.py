from app import db
from app.models.task import Task
from app.models.category import Category
from datetime import datetime

class TaskService:
    """Servicio para manejar las operaciones CRUD y lógicas de las tareas."""

    @staticmethod
    def create_task(title, description, due_date, user_id, category_ids=None):
        """Crear una nueva tarea con categorías asociadas.
        
        Args:
            title (str): El título de la tarea.
            description (str): La descripción de la tarea.
            due_date (datetime): Fecha límite para completar la tarea.
            user_id (int): ID del usuario que crea la tarea.
            category_ids (List[int], opcional): Lista de IDs de categorías a asociar.

        Returns:
            Task: La nueva tarea creada.

        Raises:
            ValueError: Si las categorías especificadas no existen.
        """
        # Obtener las categorías asociadas filtrando por los IDs proporcionados
        categories = Category.query.filter(Category.id.in_(category_ids)).all() if category_ids else []

        # Crear una nueva instancia de Task con los datos proporcionados
        new_task = Task(
            title=title,
            description=description,
            due_date=due_date,
            user_id=user_id
        )

        # Asociar las categorías a la tarea
        new_task.categories = categories

        # Agregar la nueva tarea a la sesión de base de datos
        db.session.add(new_task)
        
        # Confirmar los cambios y guardar la nueva tarea en la base de datos
        db.session.commit()
        
        return new_task

    @staticmethod
    def update_task(task_id, title=None, description=None, status=None, due_date=None, category_ids=None):
        """Actualizar los detalles de una tarea existente.
        
        Args:
            task_id (int): El ID de la tarea a actualizar.
            title (str, opcional): Nuevo título de la tarea.
            description (str, opcional): Nueva descripción de la tarea.
            status (str, opcional): Nuevo estado de la tarea ('pending', 'in-progress', 'completed').
            due_date (datetime, opcional): Nueva fecha límite para la tarea.
            category_ids (List[int], opcional): Lista de nuevos IDs de categorías asociadas.

        Returns:
            Task: La tarea actualizada.

        Raises:
            ValueError: Si la tarea no se encuentra.
        """
        # Buscar la tarea por su ID
        task = Task.query.get(task_id)
        
        # Si la tarea no existe, lanzar un error
        if not task:
            raise ValueError('Task not found')
        
        # Si se proporcionó un nuevo título, actualizarlo
        if title:
            task.title = title
        
        # Si se proporcionó una nueva descripción, actualizarla
        if description:
            task.description = description
        
        # Si se proporcionó un nuevo estado, actualizarlo
        if status:
            task.status = status
        
        # Si se proporcionó una nueva fecha límite, actualizarla
        if due_date:
            task.due_date = due_date
        
        # Si se proporcionaron nuevas categorías, actualizarlas
        if category_ids:
            categories = Category.query.filter(Category.id.in_(category_ids)).all()
            task.categories = categories
        
        # Confirmar los cambios y actualizar la tarea en la base de datos
        db.session.commit()
        
        return task

    @staticmethod
    def delete_task(task_id):
        """Eliminar una tarea existente.
        
        Args:
            task_id (int): El ID de la tarea a eliminar.

        Raises:
            ValueError: Si la tarea no se encuentra.
        """
        # Buscar la tarea por su ID
        task = Task.query.get(task_id)
        
        # Si la tarea no existe, lanzar un error
        if not task:
            raise ValueError('Task not found')
        
        # Eliminar la tarea de la base de datos
        db.session.delete(task)
        
        # Confirmar los cambios
        db.session.commit()

    @staticmethod
    def get_all_tasks():
        """Obtener todas las tareas existentes.
        
        Returns:
            List[Task]: Lista de todas las tareas en la base de datos.
        """
        # Devolver todas las tareas almacenadas
        return Task.query.all()

    @staticmethod
    def mark_task_status(task_id, status):
        """Actualizar el estado de una tarea.
        
        Args:
            task_id (int): El ID de la tarea a actualizar.
            status (str): Nuevo estado de la tarea ('pending', 'in-progress', 'completed').

        Returns:
            Task: La tarea con el estado actualizado.

        Raises:
            ValueError: Si la tarea no se encuentra.
        """
        # Buscar la tarea por su ID
        task = Task.query.get(task_id)
        
        # Si la tarea no existe, lanzar un error
        if not task:
            raise ValueError('Task not found')
        
        # Actualizar el estado de la tarea
        task.status = status
        
        # Confirmar los cambios
        db.session.commit()
        
        return task
