# Python program killing
# thread using daemon
# spp.py in coral

import threading
import time
import math
import board
import pwmio
import sys
from adafruit_motor import servo


pwm1 = pwmio.PWMOut(board.PWM1, frequency=50)
pwm2 = pwmio.PWMOut(board.PWM2, frequency=50)

# Create a servo object, my_servo.

my_servo_1 = servo.Servo(pwm1, actuation_range=360,
                         min_pulse=500, max_pulse=2500)  # pan motion
my_servo_2 = servo.Servo(pwm2, actuation_range=270,
                         min_pulse=500, max_pulse=2500)  # tilt motion
previous_tilts= [90]
list_p = [0]
counter =0


present_pan = [45,90,135,180,135,90,45,0]


def exp_increment(a,aa):
    s = 0.03* aa + 2.5
    tell = math.exp((-0.07*a)+s) + 0.6
    return tell

def log_increment(b, bb):
    s = 0.0069 * bb + 3.1
    say = -math.exp((-0.0069*b)+ s)+23
    return say

def print_angle(x,xx,y,counter=0):
    if x != y:
        while int(x) < y:
            var = exp_increment(x,xx)
            var = round(var,2)
            my_servo_2.angle = x
            time.sleep(0.001)
            x +=  var
            counter += 1
            print(var)
            print("count ", counter)
            print("x : ",x)
        while int(x) > y:
            var = log_increment(x,y)
            var = round(var,2)
            my_servo_2.angle = x
            time.sleep(0.05)
            x -=  var
            counter += 1
            print(var)
            print("count ", counter)
            print("x : ",x)

def pan_servo_control(current_pan_angle,pan_counter):


   list_p.append(current_pan_angle)
   print("previous pan angles : ", list_p)
   print(pan_counter)
   previous_pan_angle = list_p[pan_counter-1]

   while previous_pan_angle != current_pan_angle:

        if previous_pan_angle < current_pan_angle:
            for i in range(previous_pan_angle, current_pan_angle+5, 5):
                my_servo_1.angle = i
                time.sleep(0.05)
                print("pan angle ## ", i)
                previous_pan_angle = i

        if previous_pan_angle > current_pan_angle:
            for j in range(previous_pan_angle, current_pan_angle-5, -5):
                my_servo_1.angle = j
                time.sleep(0.05)
                print("pan angle ## ", j)
                previous_pan_angle = j



def func(special_counter = 0, pan_counter = 1):
    while True:
        pan_servo_control(present_pan[special_counter],pan_counter)
        pan_counter += 1
        special_counter += 1
        if special_counter == 8:
            special_counter = 0
        time.sleep(3)
        print('Thread alive, but it will die on program termination')

def func2(counter = 0):
    
    while 1: 
       present_pan = int(input("tilt angle"))
       time.sleep(1)
       previous_tilts.append(present_pan)
       print_angle(previous_tilts[counter],previous_tilts[counter],present_pan)
       counter += 1
 
def min2sec(var):
    return var*60

dur = int(input("enter duration in minutes you want to operate in "))
sec = min2sec(dur)
t1 = threading.Thread(target=func)
t1.daemon = True
t2 = threading.Thread(target = func2)
t2.daemon = True
t1.start()
t2.start()
time.sleep(sec)
sys.exit()