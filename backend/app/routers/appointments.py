from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from .. import models, schemas
from ..database import get_db


router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/", response_model=list[schemas.Appointment])
def list_appointments(day: date | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Appointment)
    if day is not None:
        q = q.filter(models.Appointment.fecha == day)
    return q.order_by(models.Appointment.fecha, models.Appointment.hora_inicio).all()


@router.post("/", response_model=schemas.Appointment, status_code=201)
def create_appointment(payload: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    if not db.get(models.Pet, payload.pet_id):
        raise HTTPException(400, "Pet not found")
    conflict = db.query(models.Appointment).filter(
        models.Appointment.vet == payload.vet,
        models.Appointment.fecha == payload.fecha,
        models.Appointment.hora_inicio < payload.hora_fin,
        models.Appointment.hora_fin > payload.hora_inicio,
    ).first()
    if conflict:
        raise HTTPException(409, "Time conflict for this vet")
    data = payload.model_dump()
    for k in ("motivo", "estado"):
        if isinstance(data.get(k), str) and data[k] == "":
            data[k] = None
    appt = models.Appointment(**data)
    db.add(appt); db.commit(); db.refresh(appt)
    return appt

@router.put("/{appt_id}", response_model=schemas.Appointment)
def update_appointment(appt_id: int, payload: schemas.AppointmentPartialUpdate, db: Session = Depends(get_db)):
    appt = db.get(models.Appointment, appt_id)
    if not appt:
        raise HTTPException(404, "Appointment not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        if isinstance(v, str) and v == "":
            v = None
        setattr(appt, k, v)
    db.commit()
    db.refresh(appt)
    return appt



@router.put("/{appt_id}/status", response_model=schemas.Appointment)
def update_status(appt_id: int, payload: schemas.AppointmentStatusUpdate, db: Session = Depends(get_db)):
    appt = db.get(models.Appointment, appt_id)
    if not appt:
        raise HTTPException(404, "Appointment not found")
    appt.estado = payload.estado
    db.commit()
    db.refresh(appt)
    return appt