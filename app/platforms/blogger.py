
import httpx
from html import escape

from app.config import settings
from app.platforms.base import BasePlatform


class BloggerPlatform(BasePlatform):

    TOKEN_URL = "https://oauth2.googleapis.com/token"
    API_URL = "https://www.googleapis.com/blogger/v3"

    async def publish(self, message: str) -> dict:

        required_settings = [
            settings.blogger_client_id,
            settings.blogger_client_secret,
            settings.blogger_refresh_token,
            settings.blogger_blog_id,
        ]

        if not all(required_settings):
            return {
                "platform": "Blogger",
                "status": "failed",
                "error": "Blogger credentials are not configured",
            }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:

                # Refresh Google access token
                token_response = await client.post(
                    self.TOKEN_URL,
                    data={
                        "client_id": settings.blogger_client_id,
                        "client_secret": settings.blogger_client_secret,
                        "refresh_token": settings.blogger_refresh_token,
                        "grant_type": "refresh_token",
                    },
                )

                token_response.raise_for_status()
                access_token = token_response.json()["access_token"]

                # Prepare Blogger post content
                content = escape(message).replace("\n", "<br>")

                # Publish post
                response = await client.post(
                    f"{self.API_URL}/blogs/"
                    f"{settings.blogger_blog_id}/posts/",
                    headers={
                        "Authorization": f"Bearer {access_token}"
                    },
                    json={
                        "kind": "blogger#post",
                        "blog": {"id": settings.blogger_blog_id},
                        "title": "Automated Update",
                        "content": content,
                    },
                )

                response.raise_for_status()
                data = response.json()

                return {
                    "platform": "Blogger",
                    "status": "success",
                    "posted_url": data.get("url"),
                    "public_access": True,
                    "error": None,
                }

        except httpx.HTTPStatusError as error:
            return {
                "platform": "Blogger",
                "status": "failed",
                "error": (
                    f"Blogger API error: "
                    f"{error.response.status_code} - "
                    f"{error.response.text}"
                ),
            }

        except (httpx.RequestError, KeyError) as error:
            return {
                "platform": "Blogger",
                "status": "failed",
                "error": str(error),
            }
