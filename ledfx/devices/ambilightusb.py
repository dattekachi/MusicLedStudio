import logging

import serial
import voluptuous as vol

from ledfx.devices import SerialDevice, packets
from ledfx.events import DevicesUpdatedEvent

_LOGGER = logging.getLogger(__name__)

COLOR_ORDERS = [
    "RGB",
    "RBG",
    "GRB",
    "BRG",
    "GBR",
    "BGR",
]


class AmbilightUsbDevice(SerialDevice):
    """AmbilightUsb device support"""

    @staticmethod
    @property
    def CONFIG_SCHEMA():
        return vol.Schema(
            {
                vol.Required(
                    "pixel_count",
                    description="Number of individual pixels",
                    default=1,
                ): vol.All(int, vol.Range(min=1)),
                vol.Required(
                    "color_order", description="Color order", default="RGB"
                ): vol.In(list(COLOR_ORDERS)),
            }
        )

    def __init__(self, ledfx, config):
        super().__init__(ledfx, config)
        self._device_type = "Ambilight USB"
        self.color_order = self._config["color_order"]

    def flush(self, data):
        try:
            self.serial.write(
                packets.build_ambilightusb_packet(data, self.color_order)
            )

        except serial.SerialException:
            # If we have lost connection, log it, go offline, and fire an event to the frontend
            _LOGGER.warning(
                "Serial Connection Interrupted. Please check connections and ensure your device is functioning correctly."
            )
            self.deactivate()
            self._ledfx.events.fire_event(DevicesUpdatedEvent(self.id))
