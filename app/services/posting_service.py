
import asyncio
from datetime import datetime

from app.platforms.discord import DiscordPlatform
from app.platforms.bluesky import BlueskyPlatform
from app.platforms.blogger import BloggerPlatform


PLATFORMS = [
    DiscordPlatform(),
    BlueskyPlatform(),
    BloggerPlatform(),
]


async def publish_on_platform(platform, message: str) -> dict:
    attempted_at = datetime.now().astimezone()

    try:
        result = await platform.publish(message)

        return {
            "platform": result.get("platform", platform.__class__.__name__),
            "status": result.get("status", "failed"),
            "posted_url": result.get("posted_url"),
            "public_access": result.get("public_access", False),
            "date": attempted_at.date(),
            "time": attempted_at.time().replace(microsecond=0),
            "error": result.get("error"),
        }

    except Exception as error:
        return {
            "platform": platform.__class__.__name__,
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": attempted_at.date(),
            "time": attempted_at.time().replace(microsecond=0),
            "error": str(error),
        }


async def publish_to_all(message: str) -> dict:
    results = await asyncio.gather(
        *[
            publish_on_platform(platform, message)
            for platform in PLATFORMS
        ]
    )

    return {
        "success": any(
            result["status"] == "success" for result in results
        ),
        "results": results,
    }
