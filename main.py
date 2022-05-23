from microbit import *

while 1:
    if button_a.get_presses():
        print("a")
    if button_b.get_presses():
        print("b")
    if accelerometer.was_gesture("shake"):
        print("m")


