import logging
from json import JSONDecodeError

from aiohttp import web

from mls.api import RestEndpoint
from mls.config import save_config
from mls.utils import (
    generate_default_config,
    generate_defaults,
    generate_id,
    inject_missing_default_keys,
)
from mls.virtuals import update_effect_config

_LOGGER = logging.getLogger(__name__)


class VirtualPresetsEndpoint(RestEndpoint):
    ENDPOINT_PATH = "/api/virtuals/{virtual_id}/presets"

    async def get(self, virtual_id) -> web.Response:
        """
        Get presets for active effect of a virtual

        Parameters:
        - virtual_id: The ID of the virtual

        Returns:
        - web.Response: The response containing the presets for the active effect of the virtual
        """
        virtual = self._mls.virtuals.get(virtual_id)
        if virtual is None:
            return await self.invalid_request(
                f"Virtual with ID {virtual_id} not found"
            )

        if not virtual.active_effect:
            return await self.invalid_request(
                f"Virtual {virtual_id} has no active effect"
            )
        effect_id = virtual.active_effect.type

        default = generate_defaults(
            self._mls.config["mls_presets"], self._mls.effects, effect_id
        )

        if effect_id in self._mls.config["user_presets"].keys():
            custom = self._mls.config["user_presets"][effect_id]
        else:
            custom = {}

        custom = inject_missing_default_keys(custom, default)

        response = {
            "status": "success",
            "virtual": virtual_id,
            "effect": effect_id,
            "mls_presets": default,
            "user_presets": custom,
        }
        return await self.bare_request_success(response)

    async def put(self, virtual_id, request) -> web.Response:
        """Set active effect of virtual to a preset.

        Args:
            virtual_id (str): The ID of the virtual.
            request (web.Request): The request object containing `category`, `effect_id`, and `preset_id`.

        Returns:
            web.Response: The HTTP response object.

        Raises:
            JSONDecodeError: If there is an error decoding the JSON data.
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
        category = data.get("category")
        effect_id = data.get("effect_id")
        preset_id = data.get("preset_id")

        missing_attributes = []

        if category is None:
            missing_attributes.append("category")
        if preset_id is None:
            missing_attributes.append("preset_id")
        if effect_id is None:
            missing_attributes.append("effect_id")

        if missing_attributes:
            return await self.invalid_request(
                f'Required attributes {", ".join(missing_attributes)} were not provided'
            )

        if category not in ["mls_presets", "user_presets"]:
            return await self.invalid_request(
                f'Category {category} is not "mls_presets" or "user_presets"'
            )

        if category == "mls_presets" and preset_id == "reset":
            effect_config = generate_default_config(
                self._mls.effects, effect_id
            )
        else:
            if effect_id not in self._mls.config[category].keys():
                return await self.invalid_request(
                    f"Effect {effect_id} does not exist in category {category}"
                )
            if preset_id not in self._mls.config[category][effect_id].keys():
                return await self.invalid_request(
                    f"Preset {preset_id} does not exist for effect {effect_id} in category {category}"
                )
            else:
                # Create the effect and add it to the virtual
                effect_config = self._mls.config[category][effect_id][
                    preset_id
                ]["config"]

        effect = self._mls.effects.create(
            mls=self._mls, type=effect_id, config=effect_config
        )
        try:
            virtual.set_effect(effect)
        except (ValueError, RuntimeError) as msg:
            error_message = (
                f"Unable to set effect on virtual {virtual.id}: {msg}"
            )
            _LOGGER.warning(error_message)
            return await self.internal_error(error_message, "error")

        update_effect_config(self._mls.config, virtual_id, effect)

        save_config(
            config=self._mls.config,
            config_dir=self._mls.config_dir,
        )

        effect_response = {}
        effect_response["config"] = effect.config
        effect_response["name"] = effect.name
        effect_response["type"] = effect.type

        response = {"status": "success", "effect": effect_response}
        return await self.bare_request_success(response)

    async def post(self, virtual_id, request) -> web.Response:
        """
        Save configuration of active virtual effect as a user preset.

        Args:
            virtual_id (str): The ID of the virtual effect.
            request (web.Request): The request object containing the new preset `name`.

        Returns:
            web.Response: The HTTP response object.


        """
        virtual = self._mls.virtuals.get(virtual_id)
        if virtual is None:
            return await self.invalid_request(
                f"Virtual with ID {virtual_id} not found"
            )

        if not virtual.active_effect:
            return await self.invalid_request(
                f"Virtual {virtual_id} has no active effect"
            )

        try:
            data = await request.json()
        except JSONDecodeError:
            return await self.json_decode_error()
        preset_name = data.get("name")
        if preset_name is None:
            return await self.invalid_request(
                'Required attribute "name" was not provided'
            )

        preset_id = generate_id(preset_name)
        effect_id = virtual.active_effect.type

        # If no presets for the effect, create a dict to store them
        if effect_id not in self._mls.config["user_presets"].keys():
            self._mls.config["user_presets"][effect_id] = {}

        # Update the preset if it already exists, else create it
        self._mls.config["user_presets"][effect_id][preset_id] = {}
        self._mls.config["user_presets"][effect_id][preset_id][
            "name"
        ] = preset_name
        self._mls.config["user_presets"][effect_id][preset_id][
            "config"
        ] = virtual.active_effect.config

        save_config(
            config=self._mls.config,
            config_dir=self._mls.config_dir,
        )

        response = {
            "status": "success",
            "preset": {
                "id": preset_id,
                "name": preset_name,
                "config": virtual.active_effect.config,
            },
        }
        return await self.bare_request_success(response)

    async def delete(self, virtual_id) -> web.Response:
        """Delete a virtual preset.

        Args:
            virtual_id (str): The ID of the virtual preset to delete.

        Returns:
            web.Response: The response indicating the success of the deletion.
        """
        virtual = self._mls.virtuals.get(virtual_id)
        if virtual is None:
            return await self.invalid_request(
                f"Virtual with ID {virtual_id} not found"
            )

        # Clear the effect
        virtual.clear_effect()

        for virtual in self._mls.config["virtuals"]:
            if virtual["id"] == virtual_id:
                if "effect" in virtual:
                    del virtual["effect"]
                    break
        save_config(
            config=self._mls.config,
            config_dir=self._mls.config_dir,
        )

        response = {"status": "success", "effect": {}}
        return await self.bare_request_success(response)
