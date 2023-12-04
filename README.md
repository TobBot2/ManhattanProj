# MANHATTAN PROJECT

This is the repository for my Manhattan Project. Despite what the name may suggest, it is not a bomb. The code in this repository is for programming the individually addressable neopixel lights for my map of Manhattan's subway system

The physical map is made of thin plywood and acrylic laser cut to the shape of Manhattan with holes where the subway lines go. Behind the holes are individually addressable led strips programmed to create interesting patterns.

The laser cutting files are also included in the `svg` folder.

### Electrial Components:
- [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/#find-reseller) 
- Led strip [WESIRI WS2812B ](https://www.amazon.com/dp/B07C1VJ1WS?psc=1&ref=ppx_yo2ov_dt_b_product_details) (amazon)
- Power supply [BTF-Lighting 12V 9A](https://www.amazon.com/dp/B01D8FM71S?psc=1&ref=ppx_yo2ov_dt_b_product_details) (amazon)
- 12V -> 5V Buck Converter
- \+ Miscellaneous buttons, wires, resistors, etc.

### Supplies:
- 1/8th inch plywood (4x4', cut into 18x32" pieces)
- 1/10th inch acrylic (18x32")
- *Wood glue?*
- *Epoxy?*
- *Stain?*
- *Wall mount?*

## Setup
### Raspberry pi pico ([full details here](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html))
1. Download this [uf2 file](https://micropython.org/download/rp2-pico/rp2-pico-latest.uf2) (or [this one](https://micropython.org/download/rp2-pico-w/rp2-pico-w-latest.uf2) for the pico W).
2. Plug in the raspberry pi pico into your computer while holding the BOOTSEL button down.
3. Drag the uf2 file into the pico's drive.
4. Download the [mu editor](https://codewith.mu/en/download).
5. Set the mode to RP2040.
6. Open and run `main.py`. This will upload the file to the pico.

Now, wherenever the pico is powered on from any source, the script `main.py` will be run.

### Wiring

*in progress*

### Laser Cutting

The laser cutting files can be found in the `svg` folder. Only cut the files that say 'cut' at the end, as the others are Inkscape files with extra metadata that doesn't always play well with other software.

**!! BEFORE YOU CUT !!** make sure there are no artifacts. I have had issues where duplicate lines create extra artifacts elsewhere on the cut, and I'm not sure if I got rid of them all on the provided files. 

*the rest is in progress*

### Extra
Currently checking out the MTA api to have a mode where it shows the realtime position of trains. To run `mtaapi.py`, make sure to get an api key from [api.mta.info](https://api.mta.info).

Also make sure to install the following pip dependencies:
- `nyct-gtfs`