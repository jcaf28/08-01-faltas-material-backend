# app/crud/__init__.py

from .crud_proyecto import get_proyecto, get_proyectos
from .crud_vertice import get_vertice, get_vertices, get_vertices_by_proyecto
from .crud_bogie import get_bogie, get_bogies, get_bogies_by_vertice
