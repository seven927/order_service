from .order import Order
from .order_repository import OrderRepository
from .order_queue_service import OrderQueueService
import httpx
from typing import Any
from ..cutomeError import NotEnoughProductError

class OrderService:
    def __init__(self, repo: OrderRepository, queue: OrderQueueService, client: httpx.AsyncClient):
        self.repo = repo
        self.queue = queue
        self.client = client
    async def get_order(self, order_id: str)->Order:
        return await self.repo.get_order(order_id)
    async def get_orders(self, page_number: int)->list[Order]:
        return await self.repo.get_orders_simple(page_number)
    async def place_order(self, inventory_id: str, product_id: str, count: int)->str:
        response: httpx.Response
        remaining_count: int
        try:
            response = await self.client.get(f"http://localhost:8000/v1/inventory/{inventory_id}/products/{product_id}/Count")
            response.raise_for_status()
            remaining_count = int(response.text)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

        if count>remaining_count:
            raise NotEnoughProductError("")
        
        new_count = remaining_count - count

        try:
            response = await self.client.post(f"http://localhost:8000/v1/inventory/{inventory_id}/products/{product_id}/Count", 
                                              json= {"quantity": new_count, "original_quantity": remaining_count})
        except Exception as e:
            raise Exception(f"An error ocurred: {e}")
        

        result = await self.repo.place_order(inventory_id, product_id, count)
        await self.queue.addPlacedOrder(result)
        return result

