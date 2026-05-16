"""Receive Truenas alert events via webhook."""

import asyncio
import logging
from typing import Any

from aiohttp import web

logger = logging.getLogger(__name__)


async def main(queue: asyncio.Queue, args: dict[str, Any]) -> None:
    host = str(args.get("host", "0.0.0.0"))
    port = int(args.get("port", 5000))
    app = web.Application()

    async def _handle(request: web.Request) -> web.Response:
        try:
            payload = await request.json()
            await queue.put(dict([("truenas", payload)]))
            return web.Response(status=200, text="OK")
        except Exception as exc:
            logger.exception("Webhook error: %s", exc)
            return web.Response(status=500, text="Error")

    app.router.add_post("/", _handle)
    app.router.add_post("/webhook", _handle)
    app.router.add_get("/health", lambda r: web.Response(text="OK"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    logger.info("Listening on %s:%d", host, port)
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await runner.cleanup()
