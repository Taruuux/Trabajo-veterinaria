from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import CheckConstraint
# en class Owner:

# en class Pet:

# (opcional) en Appointment:
#


class Owner(Base):
    __table_args__ = (CheckConstraint("nombre <> ''", name="ck_owner_nombre_nonempty"),)
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    telefono = Column(String(50))
    email = Column(String(200))
    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")


class Pet(Base):
    __table_args__ = (CheckConstraint("nombre <> ''", name="ck_pet_nombre_nonempty"),)
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(200), nullable=False)
    especie = Column(String(50), default="perro")
    owner = relationship("Owner", back_populates="pets")


class Appointment(Base):
    __table_args__ = (CheckConstraint("vet <> ''", name="ck_appt_vet_nonempty"),)
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id", ondelete="CASCADE"), nullable=False)
    vet = Column(String(200), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    motivo = Column(String(500))
    estado = Column(String(50), default="pendiente")