from typing import Annotated

from fastapi import FastAPI, Request, Query
from fastapi import HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db, engine
from app.models import Base
from app.models import User, Product, Inventory, Sale, DataWarehouse
from app.schema import UserCreate, UserUpdate, DataCreate

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.exception_handler(Exception)
async def db_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An error occurred while processing your request."},
    )


Base.metadata.create_all(bind=engine)


@app.get("/users/")
def get_all_users(name: Annotated[str | None, Query(max_length=50)] = None, db: Session = Depends(get_db)):
    if name:
        return db.query(User).filter(User.name == name).first()
    return db.query(User).all()


@app.get("/users/{user_id}")
def get_user_by_email(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.put("/users/{user_id}")
def update_user_by_email(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    return {"message": "User updated successfully"}


@app.delete("/users/{user_id}")
def delete_user_by_email(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/inventory/{product_id}")
def get_inventory_by_product_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Inventory).filter(Inventory.id == product_id).first()
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product inventory not found")


@app.get("/sales/{sales_id}")
def get_sale_by_id(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale:
        return sale
    raise HTTPException(status_code=404, detail="Product inventory not found")


@app.post("/data_warehouse/")
def create_data(data: DataCreate, db: Session = Depends(get_db)):
    print(data)
    db_data = DataWarehouse(data=data.data)
    print(data)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
