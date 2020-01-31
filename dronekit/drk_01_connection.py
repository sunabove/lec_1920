# coding: utf-8
from dronekit import connect

# Connect to UDP endpoint.
vehicle = connect( 'COM6', baud=57600, wait_ready=True)
# Use returned Vehicle object to query device state - e.g. to get the mode:
print("Mode: %s" % vehicle.mode.name)