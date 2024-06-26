from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from sqlalchemy import insert, select, update, delete

from .database import conn, session, Orders, Users
from .models import Order, User

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield session
    except:
        session.rollback()
        ValueError("Database connection failed")
    finally:
        session.close_all()

app = FastAPI(lifespan=lifespan)

@app.post("/api/v1/signup", tags=["Entrance"])
async def signup(user: User):
    try:
        query = insert(Users).values(
            name=user.name,
            email=user.email,
            password=user.password
        )
        conn.execute(query)
        conn.commit()
        return status.HTTP_201_CREATED
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/login", tags=["Entrance"])
async def login(name: str, password: str):
    try:
        query = select(Users).where(Users.name == name and Users.password == password)
        result = conn.execute(query).first()
        if not result:
            raise HTTPException(status_code=400, detail="User does not exist.")
        return status.HTTP_200_OK
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/order", tags=["Orders"])
async def create_order(order: Order):
    try: 
        query = insert(Orders).values(
            id=order.id,
            username=order.username,
            email=order.email,
            description=order.description,
        )
        conn.execute(query)
        conn.commit()
        return f"Pedido criado, {order.username}, seu identificador é {order.id}"
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
@app.get("/api/v1/order/{order_id}", tags=["Orders"])
async def read_single_order(order_id: int):
    try:
        query = conn.execute(select(Orders).where(Orders.id == order_id))
        result = query.first()
        if not result:
            return {"detail": "Order not found"}, status.HTTP_204_NO_CONTENT
        return result._asdict()
    except HTTPException:
        return HTTPException(status_code=400, detail="Pedido não encontrado")

@app.get("/api/v1/order/", tags=["Orders"])
async def read_all_orders():
    try:
        query = conn.execute(select(Orders))
        result = query.fetchall()
        if result == None:
            return {'detail' : 'None item to be found'}, status.HTTP_204_NO_CONTENT
        return result._asdict()
    except Exception:
        return HTTPException(status_code=400, detail="Pedidos não encontrados")

@app.put("/api/v1/order/{order_id}", tags=["Orders"])
async def update_item(order: Order, order_id: int):
    try: 
        query = update(Orders).where(Orders.id == order_id).values(
            username=order.username,
            email=order.email,
            description=order.description
        )
        conn.execute(query)
        conn.commit()
        return status.HTTP_200_OK
    except HTTPException:
        return HTTPException(status_code=400, detail="Pedido não encontrado")

@app.delete("/api/v1/order/{order_id}", tags=["Orders"])
async def delete_order(order_id: int):
    try: 
        query = delete(Orders).where(Orders.id == order_id)
        conn.execute(query)
        conn.commit()
        return status.HTTP_200_OK
    except HTTPException:
        return HTTPException(status_code=400, detail="O pedido não encontrado")
