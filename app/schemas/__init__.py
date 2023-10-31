# app/schemas/__init__.py

from .proyecto import Proyecto, ProyectoCreate, ProyectoInDBBase
from .vertice import Vertice, VerticeCreate, VerticeInDBBase
from .bogie import Bogie, BogieCreate, BogieInDBBase
from .kit import Kit, KitCreate, KitInDBBase
from .articulo import Articulo, ArticuloCreate, ArticuloInDBBase
from .articulo_kit import ArticuloKit, ArticuloKitCreate, ArticuloKitInDBBase
from .falta import Falta, FaltaCreate, FaltaInDBBase