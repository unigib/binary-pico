import time
from machine import Pin
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB565


# Edit these values in Thonny before running the script.
number_a = 13
number_b = 5
operation = "subtract"  # Use "add" or "subtract".

MODES = (
    "8-bit unsigned",
    "Signed magnitude",
    "One's complement",
    "Two's complement",
)
RANGES = (
    (0, 255),
    (-127, 127),
    (-127, 127),
    (-128, 127),
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
warning = display.create_pen(255, 170, 70)


def encode_number(number, selected_mode):
    if selected_mode == 0:
        return number
    if selected_mode == 1:
        return abs(number) | (0x80 if number < 0 else 0)
    if selected_mode == 2:
        return (~abs(number) & 0xFF) if number < 0 else number
    return number & 0xFF


def calculate():
    if operation not in ("add", "subtract"):
        raise ValueError('operation must be "add" or "subtract"')

    calculation_mode = 3 if operation == "subtract" else mode_index
    low, high = RANGES[calculation_mode]
    if number_a < low or number_a > high:
        raise ValueError("First number is outside this mode's range")
    if number_b < low or number_b > high:
        raise ValueError("Second number is outside this mode's range")
    if calculation_mode == 0 and (number_a < 0 or number_b < 0):
        raise ValueError("Unsigned values must be between 0 and 255")

    result = number_a + number_b if operation == "add" else number_a - number_b
    overflow = result < low or result > high
    result_bits = None if overflow else "{:08b}".format(encode_number(result, calculation_mode))
    return result, overflow, result_bits


def draw_row(label, number, bits, y, is_result=False):
    display.set_pen(white if is_result else muted)
    display.text(label, 12, y + 4, 28, 2)

    if bits is None:
        display.set_pen(warning)
        display.text("OVERFLOW", 52, y, width - 100, 2)
    else:
        display.set_pen(on_bit if is_result else white)
        display.text(bits, 52, y, width - 100, 2)

    display.set_pen(muted if not is_result else white)
    decimal = str(number)
    decimal_width = display.measure_text(decimal, 2)
    display.text(decimal, width - decimal_width - 12, y + 4, decimal_width + 4, 2)


def draw_subtraction_steps(result, overflow):
    bits_a = encode_number(number_a, 3)
    bits_b = encode_number(number_b, 3)
    inverted_b = (~bits_b) & 0xFF
    negative_b = (inverted_b + 1) & 0xFF
    full_sum = bits_a + negative_b
    result_bits = full_sum & 0xFF
    negation_wraps = number_b == -128

    display.set_pen(muted)
    display.text("A - B = A + (-B)", 12, 34, width - 24, 1)

    rows = (
        ("A = " + str(number_a), bits_a),
        ("B = " + str(number_b), bits_b),
        ("NOT B", inverted_b),
        ("+ 1", 1),
        ("-B wraps" if negation_wraps else "-B = " + str(-number_b), negative_b),
        ("A+(-B)", result_bits),
    )

    for index, (label, raw) in enumerate(rows):
        y = 55 + index * 26
        display.set_pen(on_bit if index == len(rows) - 1 else white)
        display.text(label, 12, y, 80, 1)

        bits = "{:08b}".format(raw)
        display.set_pen(on_bit if index == len(rows) - 1 else white)
        display.text(bits, 100, y, 72, 1)

        if index == len(rows) - 1:
            display.set_pen(white)
            decimal = str(result)
            display.text(decimal, 190, y, 50, 1)
            carry = str(full_sum >> 8)
            display.set_pen(muted)
            display.text("carry " + carry, 244, y, 72, 1)

    display.set_pen(warning if overflow else muted)
    if overflow:
        note = "Signed overflow"
    elif negation_wraps:
        note = "Negating -128 wraps in 8 bits"
    else:
        note = "8-bit result; carry-out discarded"
    display.text(note, 12, 218, width - 24, 1)


def draw_screen():
    result, overflow, result_bits = calculate()

    display.set_pen(background)
    display.clear()

    display.set_pen(white)
    title = "Two's complement subtraction" if operation == "subtract" else MODES[mode_index]
    display.text(title, 12, 12, width - 100, 1)

    display.set_pen(muted)
    if operation == "add":
        display.text("A: MODE", width - 76, 12, 70, 1)

    if operation == "subtract":
        draw_subtraction_steps(result, overflow)
        display.update()
        return

    bits_a = "{:08b}".format(encode_number(number_a, mode_index))
    bits_b = "{:08b}".format(encode_number(number_b, mode_index))
    operator = "+" if operation == "add" else "-"
    expression = "A " + operator + " B"
    expression_width = display.measure_text(expression, 2)
    display.set_pen(white)
    display.text(expression, (width - expression_width) // 2, 34, expression_width, 2)

    draw_row("A", number_a, bits_a, 68)
    draw_row("B", number_b, bits_b, 111)
    draw_row("=", result, result_bits, 166, is_result=True)

    if overflow:
        display.set_pen(warning)
        display.text("Result outside mode range", 12, 218, width - 24, 1)

    display.update()


draw_screen()

while True:
    if operation == "add" and button_a.value() == 0:
        time.sleep_ms(30)
        if button_a.value() == 0:
            mode_index = (mode_index + 1) % len(MODES)
            draw_screen()
            while button_a.value() == 0:
                time.sleep_ms(10)
    time.sleep_ms(10)
