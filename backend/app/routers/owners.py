from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db


router = APIRouter(prefix="/owners", tags=["owners"])


@router.get("/", response_model=list[schemas.Owner])
def list_owners(db: Session = Depends(get_db)):
    return db.query(models.Owner).order_by(models.Owner.id).all()


@router.post("/", response_model=schemas.Owner, status_code=201)
def create_owner(payload: schemas.OwnerCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    for k in ("telefono", "email"):
        if isinstance(data.get(k), str) and data[k] == "":
            data[k] = None
    owner = models.Owner(**data)
    db.add(owner); db.commit(); db.refresh(owner)
    return owner




@router.get("/{owner_id}", response_model=schemas.Owner)
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Owner, owner_id)
    if not obj:
        raise HTTPException(404, "Owner not found")
    return obj