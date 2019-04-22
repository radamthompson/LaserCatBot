#!/usr/bin/env python

# LaserCatBot.py
# 9/15/18
# Adam Thompson

import pigpio, time, random

# setup hw connections
panPin = 17
tiltPin = 18
laserPin = 23

PAN_MIN = 1200
PAN_MAX = 2500

TILT_MIN = 600
TILT_MAX = 1100

#
NUM_GPIO = 32

step = [0]*NUM_GPIO
width = [0]*NUM_GPIO
mins = [0]*NUM_GPIO
maxs = [0]*NUM_GPIO

P = [panPin,tiltPin]


# initialize gpio
pi = pigpio.pi()

if not pi.connected:
	exit()

pi.set_PWM_range(17,50)
pi.set_PWM_range(18,50)

# get random pan and tilt values
for p in P:

	step[p] = random.randrange(10,30)

	if step[p] % 2 == 0:
		step[p] = -step[p]
		
	if p == 18:
		width[p] = random.randrange(TILT_MIN,TILT_MAX+1)
		mins[p] = TILT_MIN
		maxs[p] = TILT_MAX
	else:
		width[p] = random.randrange(PAN_MIN,PAN_MAX+1)
		mins[p] = PAN_MIN
		maxs[p] = PAN_MAX


# setup laser 		
pi.set_mode(laserPin,pigpio.OUTPUT)
pi.write(laserPin,0)

# run laser dance
time_stop = time.time() + 30  # 30 sec


while time.time() < time_stop:
	pi.write(laserPin,1)
	for p in P:
	
		pi.set_servo_pulsewidth(p,width[p])
#		print(p, width[p])
		
		width[p]+= step[p]
		
		if width[p]<mins[p] or width[p]>maxs[p]:
			step[p] = -step[p]
			width[p] += step[p]
			
	time.sleep(0.1)


# turn it off
for p in P:
	pi.set_servo_pulsewidth(p,0)

pi.write(laserPin,0)	
pi.stop()
