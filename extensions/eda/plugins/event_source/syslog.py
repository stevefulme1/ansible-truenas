"""Poll Truenas for events."""

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    requests = None


async def main(queue: asyncio.Queue, args: dict[str, Any]) -> None:
    host = args["host"]
    interval = int(args.get("interval", 60))
    api_key = args.get("api_key", "")
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    seen = set()
    while True:
        try:
            resp = requests.get(
                f"https://{host}/api/v1/events",
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            for item in resp.json().get("data", []):
                item_id = str(item.get("id", ""))
                if item_id and item_id not in seen:
                    seen.add(item_id)
                    await queue.put(dict([("truenas", item)]))
        except Exception as exc:
            logger.error("Error polling: %s", exc)
        await asyncio.sleep(interval)
