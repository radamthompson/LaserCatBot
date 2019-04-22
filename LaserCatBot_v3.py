#!/usr/bin/python

# LaserCatBot_v3.py
#
# v.3 - 
#
# 9/29/18
# Adam Thompson
#-------------------------------------------------------------------------
import pigpio 
import time, random

# setup hw connections
panPin = 17
tiltPin = 18
laserPin = 23

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

# setup laser 		
pi.set_mode(laserPin,pigpio.OUTPUT)
pi.write(laserPin,0)

#---------------------------------------------------------------------------------
# define laser programs
def laserProg(TILT_MAX,TILT_MIN,PAN_MAX,PAN_MIN,stop):
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

	while time.time() < stop:
		for p in P:
			pi.set_servo_pulsewidth(p,width[p])
			width[p] += step[p]
#			print(p, width[p])
			if width[p]<mins[p] or width[p]>maxs[p]:
				step[p] = -step[p]
				width[p] += step[p]
	
		time.sleep(0.15)

def coffeeHall():
	stop = time.time() + 6
	
	PAN_MIN = 2100
	PAN_MAX = 2200

	TILT_MIN = 600
	TILT_MAX = 1100
	
	laserProg(TILT_MAX,TILT_MIN,PAN_MAX,PAN_MIN,stop)

def livingArena():
	stop = time.time() + 6
	
	PAN_MIN = 2000
	PAN_MAX = 2500

	TILT_MIN = 850
	TILT_MAX = 1100
	
	laserProg(TILT_MAX,TILT_MIN,PAN_MAX,PAN_MIN,stop)
	
def foyer():
	stop = time.time() + 6
	
	PAN_MIN = 800
	PAN_MAX = 1100

	TILT_MIN = 850
	TILT_MAX = 1100
	
	laserProg(TILT_MAX,TILT_MIN,PAN_MAX,PAN_MIN,stop)

def hall():
	stop = time.time() + 6
	
	PAN_MIN = 1100
	PAN_MAX = 1250

	TILT_MIN = 750
	TILT_MAX = 1050
	
	laserProg(TILT_MAX,TILT_MIN,PAN_MAX,PAN_MIN,stop)
	
	
def pauseLaser():
	time.sleep(3)
	
#-----------------------------------------------------------------------------	
# run laser dance
time_stop = time.time() + 60  # 1 min


while time.time() < time_stop:
	pi.write(laserPin,1)

	random.choice([foyer,hall,pauseLaser])()
			
	time.sleep(0.1)


# turn it off
for p in P:
	pi.set_servo_pulsewidth(p,0)
	a = p

pi.write(laserPin,0)	
pi.stop()
	