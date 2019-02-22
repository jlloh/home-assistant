import appdaemon.plugins.hass.hassapi as hass

from common_functions import is_no_motion

"""
Motion detected: Light on
Motion off: Light off
"""

class CommonWalkwayLight(hass.Hass):
  sensor = "binary_sensor.motion_sensor_158d0001ae94f6"
  light = "switch.wall_switch_right_158d0002ec68c0" 

  def initialize(self):
    self.listen_state(self.control_light, self.sensor) 

  def control_light(self, entity, attribute, old, new, kwargs):
    light_state = self.get_state(self.light)
    if old != new and self.sun_down():
      if new == "on" and light_state == "off":
        self.log("turning on walkway light")
        handle = self.run_in(self.lights_off, 10)
        self.turn_on(self.light)
      if new == "off" and light_state == "on":
        self.turn_off(self.light)

  def lights_off(self, kwargs):
    self.log("Turning off lights")
    self.turn_off(self.light)

