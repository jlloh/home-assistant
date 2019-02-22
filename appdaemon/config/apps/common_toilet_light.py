import appdaemon.plugins.hass.hassapi as hass

class CommonToiletLight(hass.Hass):
  toilet_sensor = "binary_sensor.motion_sensor_158d0001ae95f0"
  toilet_light = "switch.wall_switch_left_158d0002ec68c0" 
  toilet_door = "binary_sensor.door_window_sensor_158d00027b02f9"

  def initialize(self):
    self.handles = []
    self.listen_state(self.trigger_action, self.toilet_sensor)

  def trigger_action(self, entity, attribute, old, new, kwargs):
    toilet_door_state = self.get_state(self.toilet_door)
    toilet_light_state = self.get_state(self.toilet_light)
    self.log("%s, %s %s" % (old, new, self.sun_down()))
    self.log(self.handles)
    if motion_on(new, old):
        self.log("motion_detected")
        if self.sun_down() and light_is_on(toilet_light_state):
            self.log("motion detected, light on")
            self.turn_on(self.toilet_light)
    if motion_off(new, old):
        if door_closed(toilet_door_state):
            self.log("no motion but door closed. extending callback")
            handle = self.run_in(self.turn_off_light_callback, 60)
            self.handles.append(handle)
        else:
            self.log("no motion detected but door open.")
            self.turn_off(self.toilet_light)

    def turn_off_light_callback(self, entity, attribute, old, new, kwards):
        self.turn_off(self.toilet_light)

def motion_detected(new, old):
    if old == "off" and new == "on":
        return True
    return False

def motion_off(new, old):
    if old == "on" and new == "new":
        return True
    return False

def light_is_on(light_state):
    return light_state == "on"

def door_closed(door_sensor_state):
    """
    string --> boolean
    """
    if door_sensor_state == "off":
        return False
    return False
