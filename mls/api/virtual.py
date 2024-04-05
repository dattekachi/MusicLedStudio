import logging
from json import JSONDecodeError

import voluptuous as vol
from aiohttp import web

from mls.api import RestEndpoint
from mls.config import save_config
from mls.effects import DummyEffect

_LOGGER = logging.getLogger(__name__)


class VirtualEndpoint(RestEndpoint):
    """REST end-point for querying and managing virtuals"""

    ENDPOINT_PATH = "/api/virtuals/{virtual_id}"

    async def get(self, virtual_id) -> web.Response:
        """
        Get a virtual's full config
        """
        virtual = self._mls.virtuals.get(virtual_id)
        if virtual is None:
            return await self.invalid_request(
                f"Virtual with ID {virtual_id} not found"
            )

        response = {"status": "success"}
        response[virtual.id] = {
            "config": virtual.config,
            "id": virtual.id,
            "is_device": virtual.is_device,
            "auto_generated": virtual.auto_generated,
            "segments": virtual.segments,
            "pixel_count": virtual.pixel_count,
            "active": virtual.active,
            "effect": {},
        }
        # Protect from DummyEffect
        if virtual.active_effect and not isinstance(
            virtual.active_effect, DummyEffect
        ):
            effect_response = {}
            effect_response["config"] = virtual.active_effect.config
            effect_response["name"] = virtual.active_effect.name
            effect_response["type"] = virtual.active_effect.type
            response[virtual.id]["effect"] = effect_response
        return await self.bare_request_success(response)

    async def put(self, virtual_id, request) -> web.Response:
        """
        Set a virtual to active or inactive
        """
        virtual = self._mls.virtuals.get(virtual_id)
        if virtual is None:
            return await self.invalid_request(
                f"Virtual with ID {virtual_id} not found"
            )

        try:
            data = await request.json()
        except JSONDecodeError:
            return await self.json_decode_error()
        active = data.get("active")
        if active is None:
            return await self.invalid_request(
                'Required attribute "active" was not provided'
            )

        # Update the virtual's configuration
        try:
            virtual.active = active
        except ValueError as msg:
            error_message = f"Unable to set virtual {virtual.id} status: {msg}"
            _LOGGER.warning(error_message)
            return await self.internal_error(error_message, "error")

        # Update mls's config
        for idx, item in enumerate(self._mls.config["virtuals"]):
            if item["id"] == virtual.id:
                item["active"] = virtual.active
                self._mls.config["virtuals"][idx] = item
                break

        save_config(
            config=self._mls.config,
            config_dir=self._mls.config_dir,
        )

        response = {"status": "success", "active": virtual.active}
        return await self.bare_request_success(response)

    async def post(self, virtual_id, request) -> web.Response:
        """
        Update a virtual's segments configuration
        """
        virtual = self._mls.virtuals.get(virtual_id)
        if virtual is None:
            return await self.invalid_request(
                f"Virtual with ID {virtual_id} not found"
            )

        try:
            data = await request.json()
        except JSONDecodeError:
            return await self.json_decode_error()
        virtual_segments = data.get("segments")
        if virtual_segments is None:
            return await self.invalid_request(
                'Required attribute "segments" was not provided'
            )

        # Update the virtual's configuration
        old_segments = virtual.segments
        try:
            virtual.update_segments(virtual_segments)
        except (ValueError, vol.MultipleInvalid, vol.Invalid) as msg:
            error_message = (
                f"Unable to set virtual segments {virtual_segments}: {msg}"
            )
            _LOGGER.warning(error_message)
            virtual.update_segments(old_segments)
            return await self.internal_error(error_message, "error")

        # Update mls's config
        for idx, item in enumerate(self._mls.config["virtuals"]):
            if item["id"] == virtual.id:
                item["segments"] = virtual.segments
                self._mls.config["virtuals"][idx] = item
                break

        save_config(
            config=self._mls.config,
            config_dir=self._mls.config_dir,
        )

        response = {"status": "success", "segments": virtual.segments}
        return await self.bare_request_success(response)

    async def delete(self, virtual_id) -> web.Response:
        """
        Remove a virtual with this virtual id
        Handles deleting the device if the virtual is dedicated to a device
        Removes references to this virtual in any scenes
        """
        virtual = self._mls.virtuals.get(virtual_id)
        if virtual is None:
            return await self.invalid_request(
                f"Virtual with ID {virtual_id} not found"
            )

        virtual.clear_effect()
        device_id = virtual.is_device
        device = self._mls.devices.get(device_id)
        if device is not None:
            await device.remove_from_virtuals()
            self._mls.devices.destroy(device_id)

            # Update and save the configuration
            self._mls.config["devices"] = [
                _device
                for _device in self._mls.config["devices"]
                if _device["id"] != device_id
            ]

        # cleanup this virtual from any scenes
        mls_scenes = self._mls.config["scenes"].copy()
        for scene_id, scene_config in mls_scenes.items():
            self._mls.config["scenes"][scene_id]["virtuals"] = {
                _virtual_id: effect
                for _virtual_id, effect in scene_config["virtuals"].items()
                if _virtual_id != virtual_id
            }

        self._mls.virtuals.destroy(virtual_id)

        # Update and save the configuration
        self._mls.config["virtuals"] = [
            virtual
            for virtual in self._mls.config["virtuals"]
            if virtual["id"] != virtual_id
        ]
        save_config(
            config=self._mls.config,
            config_dir=self._mls.config_dir,
        )
        return await self.request_success()
