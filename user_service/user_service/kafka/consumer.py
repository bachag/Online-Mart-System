import asyncio

from aiokafka import AIOKafkaConsumer
from sqlmodel import Session
from user_service.crud import get_product_by_id
from user_service.db import engine

from user_service.kafka import _pb2

KAFKA_BROKER_URL= "broker:19092"
PRODUCT_TOPIC = "user-registered"

class KafkaConsumer:
    def __init__(self,broker_url:str,topic:str):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=broker_url,
            group_id="user_group",
            auto_offset_reset = "earliest"
        )
    async def start(self):
        await self.consumer.start()
    async def stop(self):
        await self.consumer.stop()
    async def consume(self):
        await self.start()
        try:
            async for msg in self.consumer:
                user_registered = _pb2.UserRegsitered()
                user_registered.ParseFromString(msg.value)
                session = Session(engine)
                try:
                    print(f"User Regsitered:User ID {user_registered.user_id}, Email:{user_registered.email}")
                finally:
                    session.close()
        finally:
            await self.stop()

async def run_consumer():
    consumer = KafkaConsumer(KAFKA_BROKER_URL,PRODUCT_TOPIC)
    await consumer.consume()

