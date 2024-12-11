from aiokafka import AIOKafkaProducer
from inventory_service.kafka import _pb2


KAFKA_BROKER_URL= "broker:19092"
PRODUCT_TOPIC = "inventory"

class KafkaProducer:
    def __init__(self,broker_url:str):
        self.producer = AIOKafkaProducer(bootstrap_servers=broker_url)
    async def start(self):
        await self.producer.start()
    async def stop(self):
        await self.producer.stop()
    async def send(self,topic:str,message:_pb2.InventoryUpdate):
        seralized_message = message.SerializeToString()
        await self.producer.send_and_wait(topic,seralized_message)

async def get_kafka_producer():
    producer = KafkaProducer(KAFKA_BROKER_URL)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()