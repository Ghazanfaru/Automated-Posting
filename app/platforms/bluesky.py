
import httpx

from datetime import datetime, timezone

from app.config import settings
from app.platforms.base import BasePlatform


class BlueskyPlatform(BasePlatform):

    BASE_URL = "https://bsky.social/xrpc"

    async def publish(self, message: str) -> dict:

        handle = settings.bluesky_handle
        password = settings.bluesky_app_password

        if not handle or not password:
            return {
                "platform": "Bluesky",
                "status": "failed",
                "error": "Bluesky credentials are not configured"
            }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:

                # Step 1: Authenticate and create a session
                auth_response = await client.post(
                    f"{self.BASE_URL}/com.atproto.server.createSession",
                    json={
                        "identifier": handle,
                        "password": password
                    }
                )

                auth_response.raise_for_status()
                session = auth_response.json()

                access_token = session["accessJwt"]
                did = session["did"]

                # Step 2: Create a post
                post_response = await client.post(
                    f"{self.BASE_URL}/com.atproto.repo.createRecord",
                    headers={
                        "Authorization": f"Bearer {access_token}"
                    },
                    json={
                        "repo": did,
                        "collection": "app.bsky.feed.post",
                        "record": {
                            "text": message,
                            "createdAt": datetime.now(
                                timezone.utc
                            ).isoformat().replace("+00:00", "Z")
                        }
                    }
                )

                post_response.raise_for_status()
                post_data = post_response.json()

                # Step 3: Construct public post URL
                post_uri = post_data["uri"]
                record_key = post_uri.rsplit("/", 1)[-1]

                posted_url = (
                    f"https://bsky.app/profile/{handle}/post/{record_key}"
                )

                return {
                    "platform": "Bluesky",
                    "status": "success",
                    "posted_url": posted_url,
                    "public_access": True,
                    "error": None
                }

        except httpx.HTTPStatusError as error:
            return {
                "platform": "Bluesky",
                "status": "failed",
                "error": (
                    f"Bluesky API error: "
                    f"{error.response.status_code}"
                )
            }

        except (httpx.RequestError, KeyError) as error:
            return {
                "platform": "Bluesky",
                "status": "failed",
                "error": str(error)
            }
