import board
import neopixel
import digitalio

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 8

pixels = neopixel.NeoPixel(board.GP0, num_pixels)
pixels.brightness = 0.2
hue = 0

button = digitalio.DigitalInOut(board.GP2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
button_state = False


def hsv_to_rgb(h, s, v):
    hh = None
    p = None
    q = None
    t = None
    ff = None

    i = None
    r = None
    g = None
    b = None

    if s <= 0.0:  # < is bogus, just shuts up warnings
        return (v * 255, v * 255, v * 255)
    hh = h
    if hh >= 360.0:
        hh = 0.0
    hh /= 60.0

    i = int(hh)
    ff = hh - i

    p = v * (1.0 - s)
    q = v * (1.0 - (s * ff))
    t = v * (1.0 - (s * (1.0 - ff)))

    if i == 0:
        r = v
        g = t
        b = p
    elif i == 1:
        r = q
        g = v
        b = p
    elif i == 2:
        r = p
        g = v
        b = t
    elif i == 3:
        r = p
        g = q
        b = v
    elif i == 4:
        r = t
        g = p
        b = v
    else:
        r = v
        g = p
        b = q
    return (r * 255, g * 255, b * 255)


while True:
    button_pressed = button.value
    if button_pressed != button_state and button_pressed:
        print("pressed")
    button_state = button_pressed

    hue += 2
    for i in range(len(pixels)):
        if button_state:
            pixels[i] = hsv_to_rgb((hue + i * 360 / len(pixels)) % 360, 0.8, 0.8)
        else:
            pixels[i] = (100, 100, 5)
