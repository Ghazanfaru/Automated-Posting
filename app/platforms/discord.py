
import httpx

from app.config import settings
from app.platforms.base import BasePlatform


class DiscordPlatform(BasePlatform):

    async def publish(self, message: str) -> dict:

        webhook_url = settings.discord_webhook_url

        if not webhook_url:
            return {
                "platform": "Discord",
                "status": "failed",
                "error": "Discord webhook is not configured"
            }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:

                response = await client.post(
                    webhook_url,
                    params={"wait": "true"},
                    json={"content": message}
                )

                response.raise_for_status()
                data = response.json()

                return {
                    "platform": "Discord",
                    "status": "success",
                    "posted_url": (
                        f"https://discord.com/channels/"
                        f"{data.get('guild_id')}/"
                        f"{data.get('channel_id')}/"
                        f"{data.get('id')}"
                    ),
                    "public_access": False,
                    "error": None
                }

        except httpx.HTTPStatusError as error:
            return {
                "platform": "Discord",
                "status": "failed",
                "error": f"Discord API error: {error.response.status_code}"
            }

        except httpx.RequestError as error:
            return {
                "platform": "Discord",
                "status": "failed",
                "error": f"Connection error: {str(error)}"
            }
