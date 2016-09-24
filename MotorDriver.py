# Please refer to the licensing terms stated in the README.md section of
# https://github.com/hummingworksllc/motordriver

import RPi.GPIO as GPIO, Tkinter

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

def cleanup():
    stop()
    GPIO.cleanup()

def stop():
    LF.ChangeDutyCycle(0)
    LR.ChangeDutyCycle(0)
    RF.ChangeDutyCycle(0)
    RR.ChangeDutyCycle(0)

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

def spinLeft(speed):
    LF.ChangeDutyCycle(0)
    LR.ChangeDutyCycle(speed)
    RF.ChangeDutyCycle(speed)
    RR.ChangeDutyCycle(0)
    LR.ChangeFrequency(speed + 5)
    RF.ChangeFrequency(speed + 5)

def spinRight(speed):
    LF.ChangeDutyCycle(speed)
    LR.ChangeDutyCycle(0)
    RF.ChangeDutyCycle(0)
    RR.ChangeDutyCycle(speed)
    LF.ChangeFrequency(speed + 5)
    RR.ChangeFrequency(speed + 5)

root = Tkinter.Tk()

init()

spd = Tkinter.IntVar()
spd.set(0)

dr = Tkinter.IntVar()
dr.set(1)

def change_spd(s):
    if(dr.get() == 0):
        forward(spd.get())
        lbl.config(text = 'Speed = %.2f' % spd.get())
    elif(dr.get() == 1):
        stop()
        lbl.config(text = 'Stop')
    elif(dr.get() == 2):
        reverse(spd.get())
        lbl.config(text = 'Speed = %.2f' % spd.get())

def change_dr(d):
    if(dr.get() == 0):
        stop()
        spd.set(0)
        lbl.config(text = 'Forward')
    elif(dr.get() == 1):
        stop()
        spd.set(0)
        lbl.config(text = 'Stop')
    elif(dr.get() == 2):
        stop()
        spd.set(0)
        lbl.config(text = 'Reverse')

lbl = Tkinter.Label(root, text = 'Speed = %.2f' % spd.get())
lbl.pack()

drSlider = Tkinter.Scale(root, label = 'Direction', orient = 'h', from_ = 0, to = 2, showvalue = False, variable = dr, command = change_dr)
drSlider.pack()

spdSlider = Tkinter.Scale(root, label = 'Speed', orient = 'h', from_ = 0, to = 100, showvalue = False, variable = spd, command = change_spd)
spdSlider.pack()

root.mainloop()
