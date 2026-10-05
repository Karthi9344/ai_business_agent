from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import Customer


class CustomerCreate(BaseModel):
    business_id: int
    name: str
    phone: str | None = None
    email: str | None = None


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    new_customer = Customer(
        business_id=customer.business_id,
        name=customer.name,
        phone=customer.phone,
        email=customer.email
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@router.get("/")
def get_customers(
    db: Session = Depends(get_db)
):
    customers = db.query(Customer).all()

    return customers