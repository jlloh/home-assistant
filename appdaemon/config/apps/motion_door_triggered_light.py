import appdaemon.plugins.hass.hassapi as hass

from common_functions import is_no_motion

"""
door opened
motion sensor == X (ON or OFF)
turn on Y
"""

class MotionDoorTriggeredLight(hass.Hass):

  def initialize(self):
    self.sensor = self.args["sensor"]
    self.light = self.args["light"]
    self.door = self.args["door"]
    self.motion_state = self.args["motion_state"]
    self.listen_state(self.turn_on_light, self.door)
    self.listen_state(self.turn_off_light, self.sensor) 

  def turn_on_light(self, entity, attribute, old, new, kwargs):
    motion_boolean = self.get_state(self.sensor) == self.motion_state
    light_boolean = self.get_state(self.light) == "off"
    door_trigger_boolean = old != new and new == "on"
    if motion_boolean and light_boolean and door_trigger_boolean and self.sun_down():
        self.turn_on(self.light)

  def turn_off_light(self, entity, attribute, old, new, kwargs):
    light_state = self.get_state(self.light)
    no_motion = is_no_motion(old, new)
    if no_motion and self.sun_down() and light_state == "on":
      self.turn_off(self.light)
