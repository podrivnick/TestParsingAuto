import asyncio

from src.infrastructure.config_loader import load_config
from src.presentation.api.main import (
    init_api,
    run_api,
)

from .config import MConfig


async def main() -> None:
    config = load_config(MConfig)

    app = init_api(config.api.debug)
    await run_api(app, config.api)


if __name__ == "__main__":
    asyncio.run(main())
