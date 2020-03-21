import appdaemon.plugins.hass.hassapi as hass

from common_functions import is_no_motion

"""
door opened
motion sensor == X (ON or OFF)
turn on Y
turn off Y if no motion in period
turn on Y if door is_open and motion triggered
"""

def is_motion(old, new):
  if old != new and old == "off" and new == "on":
    return True
  return False


class MotionDoorTriggeredLight(hass.Hass):

  def initialize(self):
    self.sensor = self.args["sensor"]
    self.light = self.args["light"]
    self.door = self.args["door"]
    self.motion_state = self.args["motion_state"]
    self.listen_state(self.door_controller, self.door)
    self.listen_state(self.motion_controller, self.sensor) 
    self.delay_seconds = int(self.args["delay_minutes"]) * 60
    self.handle = None
    self.motion_trigger_door_state = self.args["motion_trigger_door_state"]

  def door_controller(self, entity, attribute, old, new, kwargs):
    motion_boolean = self.get_state(self.sensor) == self.motion_state
    light_boolean = self.get_state(self.light) == "off"
    door_trigger_boolean = old != new and new == "on" #door opened
    if motion_boolean and light_boolean and door_trigger_boolean and self.sun_down():
      self.log("turning on %s" % self.light)
      self.turn_on(self.light)
    if self.handle and motion_boolean:
      self.log("cancelling timer as motion detected")
      self.cancel_timer(self.handle)
      self.handle = None

  def motion_controller(self, entity, attribute, old, new, kwargs):
    light_state = self.get_state(self.light)
    no_motion = is_no_motion(old, new)
    motion = is_motion(old, new)
    self.log("triggering motion controller. no_motion is %s" % no_motion)
    if no_motion and self.sun_down() and light_state == "on":
      self.log("turning off %s later" % self.light)
      self.handle = self.run_in(self.turn_off_callback, self.delay_seconds)
    door_state_boolean = self.get_state(self.door) == self.motion_trigger_door_state
    self.log("door state boolean is %s" % door_state_boolean)
    if motion and self.sun_down() and light_state == "off" and door_state_boolean:
      self.log("motion detected while dark and door state is %s. turning on %s" % (door_state_boolean, self.light))
      self.turn_on(self.light)
    if light_state == "on" and motion and self.handle:
      self.log("light state is on and motion detected. cancelling timer")
      self.cancel_timer(self.handle)
      self.handle = None

  def turn_off_callback(self, kwargs):
    self.log("trying to turning off %s now" % self.light)
    light_is_on = self.get_state(self.light) == "on"
    if light_is_on:
      self.log("light is on. turning it off")
      self.turn_off(self.light)
