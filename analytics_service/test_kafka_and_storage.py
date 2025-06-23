import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
import kafka_consumer


@pytest.mark.asyncio
@patch("kafka_consumer.Storage")
@patch("kafka_consumer.AIOKafkaConsumer")
async def test_kafka_event_consumption_and_storage_insert(mock_kafka_consumer_class, mock_storage_class):
    fake_event = {
        "post_id": "post123",
        "user_id": "user456",
        "timestamp": datetime.utcnow().isoformat()
    }

    mock_message = MagicMock()
    mock_message.topic = "post_likes"
    mock_message.value = fake_event

    mock_consumer_instance = AsyncMock()
    mock_consumer_instance.__aiter__.return_value = [mock_message]
    mock_kafka_consumer_class.return_value = mock_consumer_instance

    mock_storage_instance = MagicMock()
    mock_storage_class.return_value = mock_storage_instance

    await kafka_consumer.consume()

    mock_storage_instance.insert_event.assert_called_once()
    _, kwargs = mock_storage_instance.insert_event.call_args
    assert kwargs["event_type"] == "like"
    assert kwargs["post_id"] == "post123"
    assert kwargs["user_id"] == "user456"
    assert isinstance(kwargs["event_time"], datetime)


@pytest.mark.asyncio
@patch("kafka_consumer.Storage")
@patch("kafka_consumer.AIOKafkaConsumer")
async def test_kafka_event_without_timestamp(mock_kafka_consumer_class, mock_storage_class):
    fake_event = {
        "post_id": "post789",
        "client_id": "clientABC"
    }

    mock_message = MagicMock()
    mock_message.topic = "post_views"
    mock_message.value = fake_event

    mock_consumer_instance = AsyncMock()
    mock_consumer_instance.__aiter__.return_value = [mock_message]
    mock_kafka_consumer_class.return_value = mock_consumer_instance

    mock_storage_instance = MagicMock()
    mock_storage_class.return_value = mock_storage_instance

    before = datetime.utcnow()
    await kafka_consumer.consume()
    after = datetime.utcnow()

    mock_storage_instance.insert_event.assert_called_once()
    _, kwargs = mock_storage_instance.insert_event.call_args

    assert kwargs["event_type"] == "view"
    assert kwargs["post_id"] == "post789"
    assert kwargs["user_id"] == "clientABC"
    assert isinstance(kwargs["event_time"], datetime)
    assert before <= kwargs["event_time"] <= after

