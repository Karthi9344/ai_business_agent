from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import Business


class BusinessCreate(BaseModel):
    name: str
    description: str | None = None
    phone: str | None = None
    address: str | None = None


router = APIRouter(
    prefix="/businesses",
    tags=["Businesses"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_business(
    business: BusinessCreate,
    db: Session = Depends(get_db)
):
    new_business = Business(
        name=business.name,
        description=business.description,
        phone=business.phone,
        address=business.address
    )

    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    return new_business

@router.get("/")
def get_businesses(
    db: Session = Depends(get_db)
):
    businesses = db.query(Business).all()

    return businesses