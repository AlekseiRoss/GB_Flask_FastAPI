from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel, Field, PositiveFloat
from typing import List
from datetime import datetime


DATABASE_URL = "sqlite:///mydatabase.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Users table
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("surname", sqlalchemy.String(50)),
    sqlalchemy.Column("email", sqlalchemy.String(100)),
    sqlalchemy.Column("password", sqlalchemy.String(100)),
)

# Orders table
orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("order_date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String(50)),
)

# Products table
products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("price", sqlalchemy.Numeric(10, 2)),
)

# Create DB
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


# User schemas
class UserCreate(BaseModel):
    name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)


class User(UserCreate):
    id: int

    class Config:
        orm_mode = True


# Order schemas
class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    order_date: datetime
    status: str = Field(..., max_length=50)


class Order(OrderCreate):
    id: int

    class Config:
        orm_mode = True


# Product schemas
class ProductCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    price: float = Field(..., gt=0, example="9.99", precision=12, scale=2)


class Product(ProductCreate):
    id: int

    class Config:
        orm_mode = True


@app.post('/users/', response_model=User, tags=["Users"])
async def create_user(user: UserCreate):
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), 'id': last_record_id}


@app.get('/users/', response_model=List[User], tags=["Users"])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User, tags=["Users"])
async def update_user(user_id: int, new_user: UserCreate):
    query = users.update().where(users.c.id == user_id).\
        values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete("/users/{user_id}", tags=["Users"])
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': f'User with id = {user_id} deleted'}


# CRUD operations for Orders
@app.post('/orders/', response_model=Order, tags=["Orders"])
async def create_order(order: OrderCreate):
    query = orders.insert().values(**order.dict())
    last_record_id = await database.execute(query)
    return {**order.dict(), 'id': last_record_id}


@app.get('/orders/', response_model=List[Order], tags=["Orders"])
async def get_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order, tags=["Orders"])
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("/orders/{order_id}", response_model=Order, tags=["Orders"])
async def update_order(order_id: int, new_order: OrderCreate):
    query = orders.update().where(orders.c.id == order_id).\
        values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}


@app.delete("/orders/{order_id}", tags=["Orders"])
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': f'Order with id = {order_id} deleted'}


# CRUD operations for Products
@app.post('/products/', response_model=Product, tags=["Products"])
async def create_product(product: ProductCreate):
    query = products.insert().values(**product.dict())
    last_record_id = await database.execute(query)
    return {**product.dict(), 'id': last_record_id}


@app.get('/products/', response_model=List[Product], tags=["Products"])
async def get_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get("/products/{product_id}", response_model=Product, tags=["Products"])
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.put("/products/{product_id}", response_model=Product, tags=["Products"])
async def update_product(product_id: int, new_product: ProductCreate):
    query = products.update().where(products.c.id == product_id).\
        values(**new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}


@app.delete("/products/{product_id}", tags=["Products"])
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': f'Product with id = {product_id} deleted'}
