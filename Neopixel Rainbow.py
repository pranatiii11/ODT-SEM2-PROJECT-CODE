from machine import Pin
from neopixel import NeoPixel
import time

np = NeoPixel(Pin(22, Pin.OUT), 16)

# Convert HSV to RGB
def hsv_to_rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = int(h60)
    f = h60 - h60f
    p = int(v * (1 - s))
    q = int(v * (1 - f * s))
    t = int(v * (1 - (1 - f) * s))
    v = int(v)

    if h60f == 0:
        return (v, t, p)
    elif h60f == 1:
        return (q, v, p)
    elif h60f == 2:
        return (p, v, t)
    elif h60f == 3:
        return (p, q, v)
    elif h60f == 4:
        return (t, p, v)
    elif h60f == 5:
        return (v, p, q)
    else:
        return (0, 0, 0)

# Rainbow cycle animation
def rainbow_cycle(wait_ms=20):
    num_pixels = len(np)
    hue_offset = 0

    while True:
        for i in range(num_pixels):
            hue = (i * 360 // num_pixels + hue_offset) % 360
            r, g, b = hsv_to_rgb(hue, 1.0, 255)
            np[i] = (r, g, b)
        np.write()
        hue_offset = (hue_offset + 5) % 360
        time.sleep_ms(wait_ms)

# Call the rainbow function
rainbow_cycle()
