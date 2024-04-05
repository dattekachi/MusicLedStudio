import logging
import os

from aiohttp import web

from mls.api import RestEndpoint
from mls.consts import PROJECT_VERSION

_LOGGER = logging.getLogger(__name__)


class InfoEndpoint(RestEndpoint):
    ENDPOINT_PATH = "/api/info"

    async def get(self) -> web.Response:
        """
        Get information about the MusicLedStudio Controller.

        Returns:
            web.Response: The response containing the controller information.
        """
        response = {
            "url": self._mls.http.base_url,
            "name": "MusicLedStudio Controller",
            "version": PROJECT_VERSION,
            "github_sha": os.getenv("GITHUB_SHA", "unknown"),
            "is_release": os.getenv("IS_RELEASE", "false").lower(),
            "developer_mode": self._mls.config["dev_mode"],
        }
        return await self.bare_request_success(response)
