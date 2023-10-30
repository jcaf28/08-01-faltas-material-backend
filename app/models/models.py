# app/models/models.py

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Modelos
class Proyecto(Base):
    __tablename__ = 'Proyectos'
    
    id_proyecto = Column(String(32), primary_key=True)
    nombre = Column(String(255))
    
    vertices = relationship('Vertice', back_populates='proyecto')

class Vertice(Base):
    __tablename__ = 'Vertices'
    
    id_vertice = Column(String(32), primary_key=True)
    id_proyecto = Column(String(32), ForeignKey('Proyectos.id_proyecto'))
    
    proyecto = relationship('Proyecto', back_populates='vertices')
    bogies = relationship('Bogie', back_populates='vertice')
    kits = relationship('Kit', back_populates='vertice')

class Bogie(Base):
    __tablename__ = 'Bogies'
    
    matricula = Column(String(32), primary_key=True)
    id_vertice = Column(String(32), ForeignKey('Vertices.id_vertice'))
    
    vertice = relationship('Vertice', back_populates='bogies')

class Kit(Base):
    __tablename__ = 'Kits'
    
    id_kit = Column(String(64), primary_key=True)
    id_vertice = Column(String(32), ForeignKey('Vertices.id_vertice'))
    edicion = Column(Integer)
    cantidad = Column(Integer)
    va_a_linea = Column(Boolean, default=False)
    
    vertice = relationship('Vertice', back_populates='kits')
    articulos = relationship('ArticuloKit', back_populates='kit')


class Articulo(Base):
    __tablename__ = 'Articulos'
    
    id_articulo = Column(String(64), primary_key=True)
    descripcion = Column(String(255))
    
    kits = relationship('ArticuloKit', back_populates='articulo')

class ArticuloKit(Base):
    __tablename__ = 'Articulos_Kits'
    
    id_articulo_kit = Column(Integer, primary_key=True, autoincrement=True)
    id_articulo = Column(String(64), ForeignKey('Articulos.id_articulo'))
    id_kit = Column(String(64), ForeignKey('Kits.id_kit'))
    cantidad = Column(Integer)
    
    articulo = relationship('Articulo', back_populates='kits')
    kit = relationship('Kit', back_populates='articulos')

class Falta(Base):
    __tablename__ = 'Faltas'
    
    id_falta = Column(Integer, primary_key=True, autoincrement=True)
    matricula_bogie = Column(String(32), ForeignKey('Bogies.matricula'))
    id_articulo_kit = Column(Integer, ForeignKey('Articulos_Kits.id_articulo_kit'))
    cantidad_faltante = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())