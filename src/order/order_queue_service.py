import aio_pika
import json

class OrderQueueService:
    def __init__(self, channel):
        self.channel = channel

    async def addPlacedOrder(self, order_id: str, product_id: str, count: int):
            order_exchange = await self.channel.declare_exchange("order", aio_pika.ExchangeType.FANOUT)
            data=json.dumps({ "order_id": order_id, "product_id": product_id, "count": count})
            await order_exchange.publish(aio_pika.Message(body=data.encode()), routing_key="")
