import aio_pika
import json

class OrderQueueService:
    def __init__(self, channel):
        self.channel = channel

    async def addPlacedOrder(self, order_id: str, product_id: str, count: int):
            queue_name = "order_queue"
            await self.channel.declare_queue(queue_name)
            data=json.dumps({ "order_id": order_id, "product_id": product_id, "count": count})
            await self.channel.default_exchange.publish(aio_pika.Message(body=data.encode()), routing_key=queue_name)
