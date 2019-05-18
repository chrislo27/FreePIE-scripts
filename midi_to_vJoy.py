import random

def update():
	global lastPedal

	data = midi[0].data
	controlNumber = data.buffer[0]
	value = data.buffer[1]
	diagnostics.watch(controlNumber)
	diagnostics.watch(value)
	if data.status == MidiStatus.Control and controlNumber == 64:
		lastPedal = filters.mapRange(data.buffer[1], 0, 127, 0, 2**15)
	vJoy[2].x = lastPedal
	
if starting:
	lastPedal = 0
	midi[0].update += update