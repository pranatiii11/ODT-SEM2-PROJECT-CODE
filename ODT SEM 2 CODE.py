# Write your code here :-)
from machine import Pin, TouchPad, PWM #importing from libraries
from neopixel import NeoPixel
import time #for delay

#defining Sensor Inputs and their respective pins
tpin = TouchPad(Pin(4))         # Touch sensor
ldr = Pin(27, Pin.IN)           # Light sensor
sound_sensor = Pin(23, Pin.IN)  # Sound sensor

#NeoPixels
np1 = NeoPixel(Pin(22), 8)      # NeoPixel 1- ring- half neopixel turs on
np2 = NeoPixel(Pin(14), 8)      # NeoPixel 2- strip- all but 2 lights

# Buzzer
buzzer = PWM(Pin(5))
buzzer.freq(1000) #defining PWM attribute
buzzer.duty(0)    #defining PWM attribute

#DC Motor Setup
motor = PWM(Pin(18))        # ENA
motor.freq(1000)            #defining PWM attribute
motor.duty(0)               #defining PWM attribute

in1 = Pin(32, Pin.OUT)      # IN1 of Motor Driver
in2 = Pin(33, Pin.OUT)      # IN2 of Motor Driver


def clear_neopixel(np): # turning neopixel off when sensor is not triggered
    for i in range(len(np)): # for loop to access each led of the neopixel individually from 0 to length/total number of lighst
        np[i] = (0, 0, 0) #off
    np.write()

def play_touch_tune(): #buzzer tune when touch sensor is triggered
    for note in [262, 330, 392]:
        buzzer.freq(note)
        buzzer.duty(512)
        time.sleep(0.2)
    buzzer.duty(0)

def play_sound_tune(): #buzzer tune when sound sensor is triggered
    for note in [523, 494, 440]:
        buzzer.freq(note)
        buzzer.duty(512)
        time.sleep(0.2)
    buzzer.duty(0)

def play_light_tune(): #buzzer tune when light sensor is triggered
    for note in [349, 392, 440]:
        buzzer.freq(note)
        buzzer.duty(512)
        time.sleep(0.2)
    buzzer.duty(0)

def single_pixel(np, color=(255, 0, 0)): #blinking a single led of the neopixel
    clear_neopixel(np)
    np[0] = color
    np.write()

def rainbow_cycle(np, wait=0.01): #moving rainbow colours displayed in the neopixel
    for j in range(50):
        for i in range(len(np)):
            idx = (i * 256 // len(np) + j) & 255
            np[i] = wheel(idx)
        np.write()
        time.sleep(wait)

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def motor_forward(): #rotating the motor
    in1.on()
    in2.off()
    motor.duty(500)

def motor_stop(): # bringing the motor to a stop
    motor.duty(0)

# Main Loop
while True:
    touchval = tpin.read() #reading sensor value
    sound = sound_sensor.value() #reading sensor value
    light = ldr.value() #reading sensor value

    print("Touch:", touchval, "Sound:", sound, "Light:", light)

    if touchval < 300:  # Touch sensor triggered
        print("Touch detected!")
        single_pixel(np1, (0, 255, 0))  # Green led blinks when touch sensor is triggered
        rainbow_cycle(np2) # neopixel 2 displays rainbow colours
        play_touch_tune() #buzzer plays a tune
        motor_forward() #motor starts rotating in intervals
        time.sleep(2)
        motor_stop()
        clear_neopixel(np1) # neopixel turned off- to create a blinking effect
        clear_neopixel(np2)

    elif sound == 1:  # Sound sensor triggered
        print("Sound detected!")
        single_pixel(np1, (0, 0, 255))  # Blue light displayed
        play_sound_tune()
        time.sleep(1)
        clear_neopixel(np1)

    elif light == 1:  # Light sensor is in the dark( 0= light , 1= dark)
        print("Lights off!")
        single_pixel(np1, (255, 255, 0))  # Yellow for Light
        play_light_tune()
        time.sleep(1)
        clear_neopixel(np1)
    else:# light is projected on the ldr
        buzzer.duty(0)

    time.sleep(0.1)
