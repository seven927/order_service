from fastapi import FastAPI, Depends, Request, Query
from typing import Annotated
from .order.order_service import OrderService
from .order.order_repository import OrderRepository
from .order.order_queue_service import OrderQueueService
from contextlib import asynccontextmanager
import httpx
import aio_pika

@asynccontextmanager
async def lifespan(app: FastAPI):
    inventory_client = httpx.AsyncClient()
    connection = await aio_pika.connect_robust("amqps://khpcrkoz:hkd-qlUD1FzCSU78F07bkUwamx-w8ylZ@moose.rmq.cloudamqp.com/khpcrkoz")
    channel = await connection.channel()
    app.state.inventory_client = inventory_client
    app.state.order_queue_channel = channel
    yield
    await inventory_client.aclose()
    await connection.close()

app = FastAPI(lifespan=lifespan)

def get_order_repo():
    return OrderRepository()

def get_order_queue_service(request: Request):
    return OrderQueueService(request.app.state.order_queue_channel)

def get_order_service(repo: Annotated[OrderRepository, Depends(get_order_repo)],
                      queue: Annotated[OrderQueueService, Depends(get_order_queue_service)],
                      request: Request): 
    return OrderService(repo, queue, request.app.state.inventory_client)

@app.post("/v1/Orders")
async def place_order(service: Annotated[OrderService, Depends(get_order_service)],
                      inventory_id: str,
                      product_id: str,
                      count: int):
    return await service.place_order(inventory_id, product_id, count)

@app.get("/v1/Orders/{order_id}")
async def get_order(service: Annotated[OrderService, Depends(get_order_service)], order_id: str):
    return await service.get_order(order_id)

@app.get("/v1/Orders")
async def get_orders(service: Annotated[OrderService, Depends(get_order_service)],
                     page_number: Annotated[int, Query()]=0):
    return await service.get_orders(page_number)


