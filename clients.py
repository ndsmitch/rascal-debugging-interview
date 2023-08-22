import requests

from config import Config


class RascalClient:
    """Base class for Rascal internal service clients
    Access is restricted through the Isopalavial Interface
    """
    def __init__(self, api_key, rid):
        self.api_key = api_key
        self.rid = rid

    def headers(self, content="application/x-www-form-urlencoded"):
        return {
            "X-API-Key": self.api_key,
            "X-Request-ID": self.rid,
            "Content-Type": content,
            "Accept": "text/plain",
        }


class FiromactalDriveClient(RascalClient):
    def warp(self, location):
        return requests.put(
            f"{Config.FiromactalDrive.uri}/warp",
            headers=self.headers(content="application/json"),
            json={"location": location}
        )

    def diagnostic(self):
        return requests.get(
            f"{Config.FiromactalDrive.uri}/diagnostic",
            headers=self.headers(),
        )


class RamistatCoreClient(RascalClient):
    def cool(self):
        return requests.put(
            f"{Config.RamistatCore.uri}/cool",
            headers=self.headers(),
        )

    def diagnostic(self):
        return requests.get(
            f"{Config.RamistatCore.uri}/diagnostic",
            headers=self.headers(),
        )
