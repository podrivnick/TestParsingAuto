from unittest.mock import (
    AsyncMock,
    patch,
)

import pytest
from faker import Faker
from fastapi import FastAPI
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
async def test_get_random_flower_success(
    mock_send_message,
    mock_start_consuming,
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    mock_send_message.return_value = None
    mock_start_consuming.return_value = None

    url = app.url_path_for("get_random_flower_handler")
    get_random_flower_photo = True
    response: Response = client.get(
        url=url,
        params={"get_random_flower_photo": get_random_flower_photo},
    )

    assert response.is_success
    json_data = response.json()

    assert len(json_data["result"][0]["flower_name"]["value"]) > 0
