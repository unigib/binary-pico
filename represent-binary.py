import time
from machine import Pin
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB565


# Change this signed decimal number to see how each format encodes it.
number = -20

MODES = (
    "8-bit unsigned",
    "Signed magnitude",
    "One's complement",
    "Two's complement",
)
RANGES = (
    "Range: 0 to 255",
    "Range: -127 to 127",
    "Range: -127 to 127",
    "Range: -128 to 127",
)

button_a = Pin(12, Pin.IN, Pin.PULL_UP)
mode_index = 0

display = PicoGraphics(
    display=DISPLAY_PICO_DISPLAY_2,
    pen_type=PEN_RGB565,
    rotate=0,
)
display.set_backlight(0.8)
display.set_font("bitmap8")

width, height = display.get_bounds()

background = display.create_pen(14, 22, 38)
white = display.create_pen(240, 245, 255)
muted = display.create_pen(145, 165, 190)
off_bit = display.create_pen(38, 53, 74)
on_bit = display.create_pen(0, 190, 170)


def encode_number(number, selected_mode):
    if selected_mode == 0:
        if abs(number) > 255:
            raise ValueError("Unsigned magnitude must be between 0 and 255")
        raw = abs(number)
        note = "Unsigned shows magnitude +" + str(raw) if number < 0 else RANGES[0]
        return raw, str(raw), note

    if selected_mode == 1:
        if number < -127 or number > 127:
            raise ValueError("Signed magnitude must be between -127 and 127")
        raw = abs(number) | (0x80 if number < 0 else 0)
        return raw, str(number), RANGES[1]

    if selected_mode == 2:
        if number < -127 or number > 127:
            raise ValueError("One's complement must be between -127 and 127")
        raw = (~abs(number) & 0xFF) if number < 0 else number
        return raw, str(number), RANGES[2]

    if number < -128 or number > 127:
        raise ValueError("Two's complement must be between -128 and 127")
    return number & 0xFF, str(number), RANGES[3]


def draw_screen():
    raw, decimal, note = encode_number(number, mode_index)
    bits = "{:08b}".format(raw)

    display.set_pen(background)
    display.clear()

    display.set_pen(white)
    display.text(MODES[mode_index], 12, 16, width - 100, 1)

    display.set_pen(muted)
    display.text("A: NEXT", width - 76, 16, 70, 1)

    box_width = 34
    box_height = 48
    gap = 4
    left = (width - (8 * box_width + 7 * gap)) // 2
    bits_y = 62

    for index, bit in enumerate(bits):
        x = left + index * (box_width + gap)
        display.set_pen(on_bit if bit == "1" else off_bit)
        display.rectangle(x, bits_y, box_width, box_height)

        display.set_pen(white)
        text_width = display.measure_text(bit, 3)
        display.text(bit, x + (box_width - text_width) // 2, bits_y + 12, scale=3)

        display.set_pen(muted)
        weight = str(1 << (7 - index))
        label_width = display.measure_text(weight, 1)
        display.text(weight, x + (box_width - label_width) // 2, bits_y + 54)

    display.set_pen(muted)
    display.text("VALUE", 12, 142, width - 24, 2)

    display.set_pen(white)
    decimal_width = display.measure_text(decimal, 5)
    display.text(decimal, (width - decimal_width) // 2, 166, scale=5)

    display.set_pen(muted)
    display.text(note, 12, 220, width - 24, 1)

    display.update()


draw_screen()

while True:
    if button_a.value() == 0:
        time.sleep_ms(30)
        if button_a.value() == 0:
            mode_index = (mode_index + 1) % len(MODES)
            draw_screen()
            while button_a.value() == 0:
                time.sleep_ms(10)
    time.sleep_ms(10)
