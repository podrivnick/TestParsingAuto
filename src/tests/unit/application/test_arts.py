from unittest.mock import (
    AsyncMock,
    patch,
)

import pytest
from faker import Faker
from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient
from httpx import Response


@patch(
    "src.infrastructure.message_broker.kafka.KafkaMessageBroker.send_message",
    new_callable=AsyncMock,
)
@patch(
    "src.infrastructure.message_broker.kafka.KafkaMessageBroker.start_consuming",
    new_callable=AsyncMock,
)
@pytest.mark.asyncio
async def test_get_random_art_success(
    mock_send_message,
    mock_start_consuming,
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    mock_send_message.return_value = None
    mock_start_consuming.return_value = None

    url = app.url_path_for("get_random_art_handler")
    art_direction = "modern"
    response: Response = client.post(url=url, json={"art_direction": art_direction})

    assert response.is_success
    json_data = response.json()

    assert json_data["result"][0]["art_direction"]["value"] == art_direction


@patch(
    "src.infrastructure.message_broker.kafka.KafkaMessageBroker.send_message",
    new_callable=AsyncMock,
)
@patch(
    "src.infrastructure.message_broker.kafka.KafkaMessageBroker.start_consuming",
    new_callable=AsyncMock,
)
@pytest.mark.asyncio
async def test_get_random_art_is_valid(
    mock_send_message,
    mock_start_consuming,
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    mock_send_message.return_value = None
    mock_start_consuming.return_value = None

    url = app.url_path_for("get_random_art_handler")
    art_direction = "modern" * 50
    response: Response = client.post(url=url, json={"art_direction": art_direction})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_data = response.json()

    assert json_data["detail"]["error"]
