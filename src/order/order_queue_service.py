import aio_pika

class OrderQueueService:
    def __init__(self, channel):
        self.channel = channel
        
    async def addPlacedOrder(self, order_id: str):
            queue_name = "order_queue"
            await self.channel.declare_queue(queue_name)
            await self.channel.default_exchange.publish(aio_pika.Message(body=order_id.encode()), routing_key=queue_name)
