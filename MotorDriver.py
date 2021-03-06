# Copyright 2018 HUMMINGWORKS LLC All Rights Reserved.

import RPi.GPIO as GPIO
from tkinter import *
import time

root = Tk()
root.title("Motor Driver")
root.geometry("300x100")

spd = IntVar()
spd.set(0)

dr = IntVar()
dr.set(1)

leftForward = 36
leftReverse = 35
rightForward = 33
rightReverse = 32

def init():
    global LF, LR, RF, RR
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(leftForward, GPIO.OUT)
    LF = GPIO.PWM(leftForward, 20)
    LF.start(0)

    GPIO.setup(leftReverse, GPIO.OUT)
    LR = GPIO.PWM(leftReverse, 20)
    LR.start(0)

    GPIO.setup(rightForward, GPIO.OUT)
    RF = GPIO.PWM(rightForward, 20)
    RF.start(0)

    GPIO.setup(rightReverse, GPIO.OUT)
    RR = GPIO.PWM(rightReverse, 20)
    RR.start(0)

def forward(speed):
    LF.ChangeDutyCycle(speed)
    LR.ChangeDutyCycle(0)
    RF.ChangeDutyCycle(speed)
    RR.ChangeDutyCycle(0)
    LF.ChangeFrequency(speed + 5)
    RF.ChangeFrequency(speed + 5)

def reverse(speed):
    LF.ChangeDutyCycle(0)
    LR.ChangeDutyCycle(speed)
    RF.ChangeDutyCycle(0)
    RR.ChangeDutyCycle(speed)
    LR.ChangeFrequency(speed + 5)
    RR.ChangeFrequency(speed + 5)

def stop():
    LF.ChangeDutyCycle(0)
    LR.ChangeDutyCycle(0)
    RF.ChangeDutyCycle(0)
    RR.ChangeDutyCycle(0)

def cleanup():
    stop()
    GPIO.cleanup()

def change_spd(s):
    if(dr.get() == 0):
        forward(spd.get())
        lbl.config(text = 'Speed = %.2f' % spd.get())
    elif(dr.get() == 1):
        stop()
        lbl.config(text = 'Direction: Stop')
    elif(dr.get() == 2):
        reverse(spd.get())
        lbl.config(text = 'Speed = %.2f' % spd.get())

def change_dr(d):
    if(dr.get() == 0):
        stop()
        spd.set(0)
        time.sleep(0.8)
        lbl.config(text = 'Direction: Forward')
    elif(dr.get() == 1):
        stop()
        spd.set(0)
        time.sleep(0.8)
        lbl.config(text = 'Direction: Stop')
    elif(dr.get() == 2):
        stop()
        spd.set(0)
        time.sleep(0.8)
        lbl.config(text = 'Direction: Reverse')

init()

lbl = Label(root, text = 'Speed = %.2f' % spd.get())
lbl.pack()

lbldr = Label(root, text = 'Direction')
lbldr.pack()

drSlider = Scale(root, length = 100, orient = 'h', from_ = 0, to = 2, showvalue = False, variable = dr, command = change_dr)
drSlider.pack()

lblspd = Label(root, text = 'Speed')
lblspd.pack()

spdSlider = Scale(root, length = 250, orient = 'h', from_ = 0, to = 100, showvalue = False, variable = spd, command = change_spd)
spdSlider.pack()

root.mainloop()
