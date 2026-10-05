from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import Product


class ProductCreate(BaseModel):
    business_id: int
    name: str
    category: str | None = None
    description: str | None = None
    price: float
    stock: int = 0
    image_url: str | None = None


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(
        business_id=product.business_id,
        name=product.name,
        category=product.category,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image_url=product.image_url
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get("/")
def get_products(
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()

    return products

@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        return {
            "message": "Product not found"
        }

    return product

@router.put("/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    existing_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not existing_product:
        return {
            "message": "Product not found"
        }

    existing_product.business_id = product.business_id
    existing_product.name = product.name
    existing_product.category = product.category
    existing_product.description = product.description
    existing_product.price = product.price
    existing_product.stock = product.stock
    existing_product.image_url = product.image_url

    db.commit()
    db.refresh(existing_product)

    return existing_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        return {
            "message": "Product not found"
        }

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }