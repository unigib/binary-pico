from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB565


# Change this value to display a different 8-bit number.
value = 0b10000010

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

bits = "{:08b}".format(value & 0xFF)

display.set_pen(background)
display.clear()

display.set_pen(white)
display.text("BINARY NUMBER", 16, 16, width - 32, 2)

display.set_pen(muted)
display.text("8-bit unsigned", 16, 44, width - 32, 2)

box_width = 34
box_height = 48
gap = 4
left = (width - (8 * box_width + 7 * gap)) // 2
bits_y = 82

for index, bit in enumerate(bits):
    x = left + index * (box_width + gap)
    display.set_pen(on_bit if bit == "1" else off_bit)
    display.rectangle(x, bits_y, box_width, box_height)

    display.set_pen(white)
    text_width = display.measure_text(bit, 3)
    display.text(bit, x + (box_width - text_width) // 2, bits_y + 12, scale=3)

    display.set_pen(muted)
    weight = 1 << (7 - index)
    label = str(weight)
    label_width = display.measure_text(label, 1)
    display.text(label, x + (box_width - label_width) // 2, bits_y + box_height + 8)

display.set_pen(muted)
display.text("DECIMAL", 16, 164, width - 32, 2)

display.set_pen(white)
decimal = str(value & 0xFF)
decimal_width = display.measure_text(decimal, 5)
display.text(decimal, (width - decimal_width) // 2, 188, scale=5)

display.update()
