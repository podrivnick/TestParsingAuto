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
async def test_get_random_poem_success(
    mock_send_message,
    mock_start_consuming,
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    mock_send_message.return_value = None
    mock_start_consuming.return_value = None

    url = app.url_path_for("get_random_poem_handler")
    poem_author = "George Orwell"
    response: Response = client.post(url=url, json={"poem_author": poem_author})

    assert response.status_code == status.HTTP_201_CREATED
    json_data = response.json()

    assert len(json_data["result"][0]["poem_author"]["value"]) > 0


@patch(
    "src.infrastructure.message_broker.kafka.KafkaMessageBroker.send_message",
    new_callable=AsyncMock,
)
@patch(
    "src.infrastructure.message_broker.kafka.KafkaMessageBroker.start_consuming",
    new_callable=AsyncMock,
)
@pytest.mark.asyncio
async def test_get_random_poem_is_valid(
    mock_send_message,
    mock_start_consuming,
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    mock_send_message.return_value = None
    mock_start_consuming.return_value = None

    url = app.url_path_for("get_random_poem_handler")
    poem_author = "George Orwell" * 50
    response: Response = client.post(url=url, json={"poem_author": poem_author})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_data = response.json()

    assert json_data["detail"]["error"]
