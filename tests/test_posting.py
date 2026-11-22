
import unittest
from unittest.mock import patch

from app.services.posting_service import publish_to_all


class FakePlatform:
    def __init__(self, name, result=None, should_raise=False):
        self.name = name
        self.result = result
        self.should_raise = should_raise

    async def publish(self, message):
        if self.should_raise:
            raise Exception("Simulated platform failure")

        return {
            "platform": self.name,
            **self.result,
        }


class PostingServiceTests(unittest.IsolatedAsyncioTestCase):

    async def test_all_platforms_succeed(self):
        platforms = [
            FakePlatform("Discord", {
                "status": "success",
                "posted_url": "https://example.com/discord",
                "public_access": False,
            }),
            FakePlatform("Bluesky", {
                "status": "success",
                "posted_url": "https://example.com/bluesky",
                "public_access": True,
            }),
        ]

        with patch(
            "app.services.posting_service.PLATFORMS",
            platforms
        ):
            response = await publish_to_all("Test https://example.com")

        self.assertTrue(response["success"])
        self.assertEqual(len(response["results"]), 2)
        self.assertTrue(
            all(r["status"] == "success" for r in response["results"])
        )

    async def test_one_platform_fails(self):
        platforms = [
            FakePlatform("Discord", {
                "status": "success",
                "posted_url": "https://example.com/discord",
                "public_access": False,
            }),
            FakePlatform("Bluesky", should_raise=True),
        ]

        with patch(
            "app.services.posting_service.PLATFORMS",
            platforms
        ):
            response = await publish_to_all("Test https://example.com")

        self.assertTrue(response["success"])
        self.assertEqual(response["results"][0]["status"], "success")
        self.assertEqual(response["results"][1]["status"], "failed")

    async def test_all_platforms_fail(self):
        platforms = [
            FakePlatform("Discord", should_raise=True),
            FakePlatform("Bluesky", should_raise=True),
        ]

        with patch(
            "app.services.posting_service.PLATFORMS",
            platforms
        ):
            response = await publish_to_all("Test https://example.com")

        self.assertFalse(response["success"])
        self.assertTrue(
            all(r["status"] == "failed" for r in response["results"])
        )


if __name__ == "__main__":
    unittest.main()
