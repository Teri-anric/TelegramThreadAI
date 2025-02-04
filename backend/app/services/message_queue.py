"""
RabbitMQ Message Queue Service for Chat Messages

This module provides an asynchronous message queue service 
for handling chat messages from different sources.
"""

import json
import logging
from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

import aio_pika
from aio_pika import DeliveryMode, ExchangeType

logger = logging.getLogger(__name__)


class MessageQueueService:
    """
    Manages RabbitMQ message queue for chat messages.
    Supports publishing and consuming messages from different sources.
    """

    def __init__(
        self,
        rabbitmq_url: str = "amqp://guest:guest@localhost/",
        exchange_name: str = "chat_messages",
    ):
        """
        Initialize the message queue service.

        :param rabbitmq_url: RabbitMQ connection URL
        :param exchange_name: Name of the exchange for routing messages
        """
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name
        self._connection: Optional[aio_pika.Connection] = None
        self._channel: Optional[aio_pika.Channel] = None

    async def connect(self):
        """
        Establish connection to RabbitMQ and create channel and exchange.
        """
        if not self._connection or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(self.rabbitmq_url)
            self._channel = await self._connection.channel()

            # Declare a topic exchange for flexible routing
            await self._channel.declare_exchange(self.exchange_name, ExchangeType.TOPIC)

    async def close(self):
        """
        Close RabbitMQ connection.
        """
        if self._connection:
            await self._connection.close()

    async def publish_message(
        self,
        chat_id: UUID,
        user_id: UUID,
        content: str,
        routing_key: Optional[str] = None,
    ):
        """
        Publish a message to the chat message exchange.

        :param chat_id: UUID of the chat
        :param user_id: UUID of the user
        :param content: Message content
        :param routing_key: Optional routing key for advanced routing
        """
        await self.connect()
        # Construct routing key if not provided
        routing_key = routing_key or f"{chat_id}"

        # Prepare message with additional metadata in headers
        message_body = json.dumps(
            {"chat_id": str(chat_id), "user_id": str(user_id), "content": content}
        ).encode()

        # Publish message using the topic exchange instead of default
        exchange = await self._channel.get_exchange(self.exchange_name)
        await exchange.publish(
            aio_pika.Message(
                body=message_body,
                headers={
                    "chat_id": str(chat_id),
                    "user_id": str(user_id),
                    "timestamp": datetime.now(UTC).isoformat(),
                },
                delivery_mode=DeliveryMode.PERSISTENT,
                content_type="application/json",
                content_encoding="utf-8",
                message_id=str(uuid4()),
            ),
            routing_key=routing_key,
        )

        logger.info(f"Message published: {routing_key}")

    async def consume_messages(self, chat_id: Optional[UUID] = None):
        """
        Consume messages from the queue with optional filtering.

        :param chat_id: Optional chat ID filter
        """
        await self.connect()

        # Create a temporary queue
        queue = await self._channel.declare_queue(exclusive=True)

        # Bind queue with appropriate routing key pattern
        routing_key_pattern = chat_id or "*"
        await queue.bind(self.exchange_name, routing_key_pattern)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body.decode())
                    yield payload


async def main():
    # Example usage
    mq_service = MessageQueueService()

    # Publishing a message
    await mq_service.publish_message(
        chat_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        message={"text": "Hello, world!"},
    )

    # Consuming messages
    async for msg in mq_service.consume_messages(
        chat_id=UUID("123e4567-e89b-12d3-a456-426614174000")
    ):
        print(msg)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
