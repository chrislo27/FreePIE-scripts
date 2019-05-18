import random

def negPos(n, p):
	if n and p:
		return 0
	elif n and not p:
		return -1
	elif p and not n:
		return 1
	else:
		return 0

def update():
	global lastPedal
	global pressedNotes

	data = midi[0].data
	buf1 = data.buffer[0]
	buf2 = data.buffer[1]
	
	volume = buf2 / 127.0
	semitone = buf1 - 60 # semitones from middle C
	
	diagnostics.watch(buf1)
	diagnostics.watch(buf2)
	
	if data.status == MidiStatus.Control and buf1 == 64: # buf1 = control change
		lastPedal = buf2 >= 64
	elif data.status == MidiStatus.NoteOn:
		if volume <= 0:
			pressedNotes[semitone] = False
		else:
			pressedNotes[semitone] = True
	elif data.status == MidiStatus.NoteOff:
		pressedNotes[semitone] = False

	# Map to keyboard (Yamaha NP-30)
	def n(semitone):
		return pressedNotes.get(semitone, False)
	
	# Reference: C is middle C, C+ is one octave up, C- is one octave down
	# Escape key (last note on keyboard)
	keyboard.setKey(Key.Escape, n(-32))
	
	# Movement:
	# W -> E (+4)
	# S -> D# (+3)
	# A -> D (+2)
	# D -> F (+5)
	# Sneak (shift) -> C (0)
	# Sprint (ctrl) -> B- (-1)
	keyboard.setKey(Key.LeftShift, n(0))
	keyboard.setKey(Key.LeftControl, n(-1))
	keyboard.setKey(Key.W, n(4))
	keyboard.setKey(Key.S, n(3))
	keyboard.setKey(Key.A, n(2))
	keyboard.setKey(Key.D, n(5))
	# Jump is damper pedal
	keyboard.setKey(Key.Space, lastPedal)
	
	# Camera:
	# C+ and G+ (+12 and +19) look left and right respectively
	# D#+ and E+ (+15 and +16) look up and down respectively
	delta = 14
	invertX = False
	invertY = False
	mouse.deltaX = delta * negPos(n(12), n(19)) * (-1 if invertX else 1)
	mouse.deltaY = delta * negPos(n(15), n(16)) * (-1 if invertY else 1)
	
	# Mouse buttons
	# D+ (+14) -> Attack (left click)
	# F+ (+17) -> Action (right click)
	mouse.leftButton = n(14)
	mouse.rightButton = n(17)
	
	# Num row for hotbar
	# On the NP-30 this corresponds to the SONG number buttons 1-10
	keyboard.setKey(Key.D1, n(-12))
	keyboard.setKey(Key.D2, n(-11))
	keyboard.setKey(Key.D3, n(-10))
	keyboard.setKey(Key.D4, n(-9))
	keyboard.setKey(Key.D5, n(-8))
	keyboard.setKey(Key.D6, n(-7))
	keyboard.setKey(Key.D7, n(-6))
	keyboard.setKey(Key.D8, n(-5))
	keyboard.setKey(Key.D9, n(-4))
	keyboard.setKey(Key.D0, n(-3))
	
	# Inventory -> A+ (+21)
	keyboard.setKey(Key.E, n(21))
	
	
if starting:
	lastPedal = False
	pressedNotes = dict() # key = semitones from middle C, value = Boolean
	midi[0].update += update