# app/crud/__init__.py

from .crud_proyecto import get_proyecto, get_proyectos
from .crud_vertice import get_vertice, get_vertices, get_vertices_by_proyecto
from .crud_bogie import get_bogie, get_bogies, get_bogies_by_vertice
from .crud_kit import get_kit, get_kits, get_kits_by_vertice
from .crud_articulo import get_articulo, get_articulos, get_articulos_by_kit
from .crud_articulo_kit import get_articulo_kit, get_articulo_kit_by_kit_id, get_articulos_kit
