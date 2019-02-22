import appdaemon.plugins.hass.hassapi as hass

from common_functions import is_no_motion

"""
door opened
motion sensor == X (ON or OFF)
turn on Y
"""

class WirelessSwitch(hass.Hass):

  def initialize(self):
    self.switch = self.args["switch"]
    self.single_click_entity = self.args["single_click_entity"]
    self.double_click_entity = self.args["double_click_entity"]
    self.listen_event(self.toggle, "xiaomi_aqara.click", entity_id=self.switch)

  def toggle(self, event_name, data, kwargs):
    if data["click_type"] == "single":
      if self.get_state(self.single_click_entity) == "on":
        self.turn_off(self.single_click_entity)
      else:
        self.turn_on(self.single_click_entity)
    if data["click_type"] == "double":
      if self.get_state(self.double_click_entity) == "on":
        self.turn_off(self.double_click_entity)
      else:
        self.turn_on(self.double_click_entity)
