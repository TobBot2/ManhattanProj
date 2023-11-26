import board
import neopixel
import digitalio

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

@dataclass
class Led: # first three args required on init
    x: float
    y: float
    index: int
    neighbors_indeces: List[int] = []
    powered: float = 0 # seconds until powered off
    intensity: float = 1

@dataclass
class SortedLed:
    led: Led
    weight: float

@dataclass
class SortedLedList:
    mode: str
    max_weight: float
    current_index: int = -1
    led_list: List[SortedLed]

class Mode(Enum):
    WHITE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    RAINBOW = 5
    SUBWAY_COLORS = 6 # official colors from mta
    BREATHE_WHITE = 7
    BREATHE_RED = 8
    BREATHE_GREEN = 9
    BREATHE_BLUE = 10
    WASH_DOWN_WHITE = 11
    WASH_DOWN_RAINBOW = 12
    SIMULATE = 13 # simulate trains going down the lines
    SIMULATE_WHITE = 14


class Speed(Enum):
    NORMAL = 1
    FAST = 2
    SLOW = 3
    SLOW_X = 4

class Train:
    current_Led: Led
    direction: bool # true is positive direction, false is negative
    """ Trains will run down a line based on current_led's next index. 
        If there are multiple, it creates a duplicate train. If there
        are none, it dies (or maybe respowns at a random line again) """

# GLOBAL VARIABLES
timer = 0
rate = 1
sorted_leds: SortedLedList = []

# NEOPIXEL SETUP
num_pixels = 8
pixels = neopixel.NeoPixel(board.GP0, num_pixels)
pixels.brightness = 0.2
hue = 0

# MODE BUTTON SETUP
mode_btn = digitalio.DigitalInOut(board.GP2)
mode_btn.direction = digitalio.Direction.INPUT
mode_btn.pull = digitalio.Pull.UP
mode_btn_state = False
mode: Mode = Mode.WHITE

# SPEED BUTTON SETUP
speed_btn = digitalio.DigitalInOut(board.GP3)
speed_btn.direction = digitalio.Direction.INPUT
speed_btn.pull = digitalio.Pull.UP
speed_brn_state = False
speed: Speed = Speed.NORMAL

""" *******************
****** LED LINES ******
******************* """
# makes a list of leds based on first and last led in the strip
def generate_strip(led1: Led, led2: Led) -> List[Led]:
    count = led2.index - led1.index
    dy = (led2.y - led1.y) / count
    dx = (led2.x - led1.x) / count

    leds = []
    for i in range(count+1): # +1 includes led2
        if i == 0:
            leds.append(Led(led1.x, led1.y, led1.index, neighbors_indeces=[i+1])) # starting led only has forward index
        elif i == count:
            leds.append(Led(led2.x, led2.y, led2.index, neighbors_indeces=[i-1])) # ending led only has previous index
        else:
            leds.append(Led(led1.x + i*dx, led1.y + i*dy, led1.index + i, neighbors_indeces=[i+1, i-1])) # normally they have forward & backwards index

    return leds

# manually enter the leds for the lines
line_123 = [*generate_strip(Led(0, 0, 0), Led(100, 0, 10)), *generate_strip(Led(73, 2, 30), Led(100, 20, 35))]   # 123 line
junction = next((x for x in line_123 if x.index == 7), None) # find led whose index is 7
if junction is not None:
    junction.next_index = 30
else:
    print("error creating junction in the 123 line")

line_456 = []

lines: Dict[str, List[Led]] = {
    "123": line_123,
    "456": line_456
}


# making functions that return sorted lists
# is silly because I'll have to loop through
# all leds anyway to decrease 'power' value.
def sort_by_x() -> List[SortedLed]:
    sorted_leds: List[SortedLed] = []
    for i in range(lines.count):
        minimum: SortedLed = None
        for key, leds in lines.items():
            for led in leds:
                # loop through all leds
                weight = led.x
                if minimum is None or (not led in sorted_leds and weight < minimum.weight):
                    sorted_leds.append(SortedLed(led, weight))

    return sorted_leds

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

    if s <= 0.0: # < is bogus, just shuts up warnings
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

def handle_mode_switch():
    button_pressed = mode_btn.value
    if button_pressed != mode_btn_state and button_pressed:
        mode = (mode + 1) % len(Mode) # loop through mode
        print("mode = ", mode)
    mode_btn_state = button_pressed

def handle_speed_switch():
    button_pressed = speed_btn.value
    if button_pressed != speed_btn_state and button_pressed:
        speed = (speed + 1) % len(Speed) # loop through speed
        print("speed = ", speed)
    speed_btn_state = button_pressed

def increase_timer():
    if speed == Speed.NORMAL:
        timer += rate
    elif speed == Speed.FAST:
        timer += rate * 2
    elif speed == Speed.SLOW:
        timer += rate / 2
    elif speed == Speed.SLOW_X:
        timer += rate / 4


def wash_effect_x(t: float):
    # make sure the sorted_leds are sorted by the correct value
    if sorted_leds.mode != "x":
        sorted_leds.mode = "x"
        sorted_leds.led_list = sort_by_x()
        sorted_leds.current_index = 0

    if sorted_leds.led_list[sorted_leds.current_index].weight < t % sorted_leds.max_weight:
        sorted_leds.led_list[sorted_leds.current_index].led.powered = 3
        sorted_leds.current_index = (sorted_leds.current_index + 1) % len(sorted_leds.led_list)
    


while True:
    handle_mode_switch()
    handle_speed_switch()

    increase_timer()

    hue += 2
    for i in range(len(pixels)):
        if mode == Mode.WHITE:
            pixels[i] = hsv_to_rgb((hue + i * 360 / len(pixels)) % 360, 0.8, 0.8)
        else:
            pixels[i] = (100, 100, 5)
