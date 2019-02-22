import appdaemon.plugins.hass.hassapi as hass

from common_functions import is_no_motion

"""
When to turn on dining room light
- When entering the house
When to turn off dining room light
- When no motion detected
"""

class DiningRoomLight(hass.Hass):
  sensor = "binary_sensor.motion_sensor_158d0002583b24"
  light = "light.dining_lights" 
  main_door = "binary_sensor.door_window_sensor_158d00027b02f9"

  def initialize(self):
    self.listen_state(self.turn_on_light, self.main_door)
    self.listen_state(self.turn_off_light, self.sensor) 

  def turn_on_light(self, entity, attribute, old, new, kwargs):
    motion_in_dining = self.get_state(self.sensor) == "on"
    light_state = self.get_state(self.light)
    self.log(light_state)
    if old == "off" and new == "on" and self.sun_down() and light_state == "off":
      if motion_in_dining:
        # door opened, motion in dining room
        self.log("door opened but motion. skipping")
        pass
      else:
        self.turn_on(self.light)

  def turn_off_light(self, entity, attribute, old, new, kwargs):
    light_state = self.get_state(self.light)
    no_motion = is_no_motion(old, new)
    if no_motion() and self.sun_down() and light_state == "on":
      self.turn_off(self.light)
