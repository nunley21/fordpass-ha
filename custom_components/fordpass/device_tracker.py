"""Vehicle Tracker Sensor"""
import logging

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity

from . import FordPassEntity
from .const import DOMAIN, COORDINATOR

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add the Entities from the config."""
    entry = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]

    # Added a check to see if the car supports GPS
    if entry.data["metrics"]["position"] is not None:
        async_add_entities([CarTracker(entry, "gps")], True)
    else:
        _LOGGER.debug("Vehicle does not support GPS")


class CarTracker(FordPassEntity, TrackerEntity):
    def __init__(self, coordinator, sensor):

        self._attr = {}
        self.sensor = sensor
        self.coordinator = coordinator
        self.data = coordinator.data["metrics"]
        self._device_id = "fordpass_tracker"
        # Required for HA 2022.7
        self.coordinator_context = object()

    @property
    def latitude(self):
        """Return latitude"""
        return float(self.data["position"]["value"]["location"]["lat"])

    @property
    def longitude(self):
        """Return longtitude"""
        return float(self.data["position"]["value"]["location"]["lon"])

    @property
    def source_type(self):
        """Set source type to GPS"""
        return SOURCE_TYPE_GPS

    @property
    def name(self):
        """Return device tracker entity name"""
        return "fordpass_tracker"

    @property
    def device_id(self):
        """Return device tracker id"""
        return self.device_id

    @property
    def extra_state_attributes(self):
        """No extra attributes to return"""
        return None

    @property
    def icon(self):
        """Return device tracker icon"""
        return "mdi:radar"