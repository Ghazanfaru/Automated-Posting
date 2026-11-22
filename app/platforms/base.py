from abc import ABC, abstractmethod

class BasePlatform(ABC):

    @abstractmethod
    async def publish(self, message: str) -> dict:

         """
        Publish a message to the platform.

        Returns platform publishing details.
        """
    pass 