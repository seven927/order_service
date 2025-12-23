from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from typing import Any
from .order import Order
from datetime import datetime

class OrderRepository:
    def __init__(self):
        self.url="mongodb+srv://eacmomo0927_db_user:vKaA49hxWXGLdVe8@mycluster.9cvhjpt.mongodb.net/?appName=MyCluster"
    async def get_order(self, order_id: str):
        client: AsyncMongoClient[dict[str, Any]] | None = None
        try:
            client = AsyncMongoClient(self.url, server_api=ServerApi('1'))
            db = client["OnlineShop"]
            result = await db["order"].find({"_id": ObjectId(order_id)})
        except Exception:
            raise Exception(f"An error occurred when getting order: {order_id}")
        finally:
            if client is not None:
                await client.close()
        if result is None:
            raise Exception("An error occurred")
        return Order(id=result["_id"], date=result["create_timestamp"], inventory_id=result["inventory_id"], product_id=result["product_id"], count=result["count"], status=result["status"])
    async def get_orders_simple(self, page_number: int)->list[Order]:
        client: AsyncMongoClient[dict[str, Any]] | None = None
        orders: list[Order] = []
        try:
            client = AsyncMongoClient(self.url, server_api=ServerApi('1'))
            db = client["OnlineShop"]
            result = db["order"].find({}).skip(page_number * 5).limit(5)
        except Exception:
            raise Exception(f"An error occurred")
        finally:
            if client is not None:
                await client.close()
        if(result is None):
            raise Exception(f"An error occurred")
        async for order in result:
            orders.append(Order(id=str(order["_id"]), date=order["create_timestamp"], inventory_id=order["inventory_id"], product_id=order["product_id"], count=order["count"],status=order["status"]))
        return orders
    async def get_orders(self, count: int, lastOrderId: str):
        pass
    async def place_order(self, inventory_id: str, product_id: str, count: int)->str:
        client: AsyncMongoClient[dict[str, Any]] | None = None
        nowInst = datetime.now()
        try:
            client = AsyncMongoClient(self.url, server_api=ServerApi('1'))
            db = client["OnlineShop"]
            result = await db["order"].insert_one({"inventory_id": inventory_id, "product_id": product_id, "create_timestamp": nowInst, "status": "active", "count": count, "last_update_timestamp": nowInst})
        except Exception as e:
            raise Exception(f"An error occurred when placing order")
        finally:
            if client is not None:
                await client.close()
        
        return str(result.inserted_id)