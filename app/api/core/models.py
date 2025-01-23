from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.db.conection_orm import Base


class Colony(Base):
    __tablename__ = 'colonies'
    index = Column(Integer, primary_key=True, autoincrement=True)  # Auto-incrementa si es necesario
    id = Column(Integer, unique=True, nullable=False)  # Debe ser único si se usa como clave foránea
    colonia = Column(String(255), nullable=False)  # Limitar longitud a 255 caracteres
    alcaldia = Column(String(255), nullable=False)  # Limitar longitud a 255 caracteres
    wifi_records = relationship("WifiRecord", back_populates="colony")  # Relación bidireccional

    def as_dict(self):
        return {"colonia": self.colonia, "alcaldia": self.alcaldia}


class WifiRecord(Base):
    __tablename__ = 'wifi_logs'
    index = Column(Integer, primary_key=True, autoincrement=True)  # Auto-incrementa si es necesario
    id = Column(String(255), nullable=False)  # Limitar longitud a 255 caracteres
    id_colonia = Column(Integer, ForeignKey('colonies.id'), nullable=True)  # Clave foránea
    programa = Column(String(255), nullable=True)  # Limitar longitud a 255 caracteres
    fecha_instalacion = Column(Float, nullable=True)  # Cambiar a `Float` o `Date` según los datos
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    colony = relationship("Colony", back_populates="wifi_records")  # Relación bidireccional

    def as_dict(self):
        return {
            "id": self.id,
            "programa": self.programa,
            "fecha_instalacion": self.fecha_instalacion,
            "latitud": self.latitud,
            "longitud": self.longitud,
        }
