def is_no_motion(old, new):
    if old != new and old == "on" and new == "off":
        return True
    return False
