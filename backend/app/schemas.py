from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict
from typing import Annotated
from datetime import date, time

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

# --- Owners ---
class OwnerCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    nombre: NonEmptyStr
    telefono: str | None = None
    email: EmailStr | None = None

class Owner(BaseModel):
    id: int
    nombre: str
    telefono: str | None = None
    email: EmailStr | None = None
    model_config = ConfigDict(from_attributes=True)

# --- Pets ---
class PetCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    owner_id: int
    nombre: NonEmptyStr
    especie: NonEmptyStr

class Pet(BaseModel):
    id: int
    owner_id: int
    nombre: str
    especie: str
    model_config = ConfigDict(from_attributes=True)

# --- Appointments ---
class AppointmentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    pet_id: int
    vet: NonEmptyStr
    fecha: date
    hora_inicio: time
    hora_fin: time
    motivo: str | None = None
    estado: str | None = None

class Appointment(BaseModel):
    id: int
    pet_id: int
    vet: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    motivo: str | None = None
    estado: str | None = None
    model_config = ConfigDict(from_attributes=True)

class AppointmentStatusUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    estado: NonEmptyStr

class AppointmentPartialUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    motivo: str | None = None
    estado: str | None = None
