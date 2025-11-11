from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db


router = APIRouter(prefix="/pets", tags=["pets"])


@router.get("/", response_model=list[schemas.Pet])
def list_pets(owner_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Pet)
    if owner_id is not None:
        q = q.filter(models.Pet.owner_id == owner_id)
    return q.order_by(models.Pet.id).all()


@router.post("/", response_model=schemas.Pet, status_code=201)
def create_pet(payload: schemas.PetCreate, db: Session = Depends(get_db)):
    if not db.get(models.Owner, payload.owner_id):
        raise HTTPException(400, "Owner not found")
    data = payload.model_dump()
    for k in ():
        pass
    pet = models.Pet(**data)
    db.add(pet); db.commit(); db.refresh(pet)
    return pet

