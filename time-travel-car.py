import time
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB565


display = PicoGraphics(
    display=DISPLAY_PICO_DISPLAY_2,
    pen_type=PEN_RGB565,
    rotate=0,
)
display.set_backlight(0.8)
display.set_font("bitmap8")

width, height = display.get_bounds()

sky = display.create_pen(6, 12, 32)
stars = display.create_pen(120, 171, 220)
horizon = display.create_pen(19, 38, 67)
road = display.create_pen(10, 17, 31)
road_line = display.create_pen(0, 157, 185)
shadow = display.create_pen(3, 7, 17)
tire = display.create_pen(25, 34, 50)
rim = display.create_pen(126, 158, 177)
body_edge = display.create_pen(255, 103, 128)
body = display.create_pen(174, 195, 205)
body_light = display.create_pen(224, 236, 237)
window = display.create_pen(15, 43, 69)
teal = display.create_pen(0, 211, 205)
amber = display.create_pen(255, 157, 74)

car_width = 120
car_x = -car_width
car_y = height - 95
road_y = height - 45

star_positions = (
    (24, 34), (72, 58), (121, 27), (171, 48),
    (216, 31), (278, 57), (301, 24), (43, 91),
    (148, 77), (250, 96),
)


def draw_car(x, y):
    display.set_pen(shadow)
    display.rectangle(x + 8, y + 42, 105, 8)

    display.set_pen(tire)
    display.rectangle(x + 20, y + 31, 20, 18)
    display.rectangle(x + 82, y + 31, 20, 18)

    display.set_pen(rim)
    display.rectangle(x + 26, y + 36, 8, 8)
    display.rectangle(x + 88, y + 36, 8, 8)

    display.set_pen(body_edge)
    display.rectangle(x + 4, y + 24, 110, 17)
    display.rectangle(x + 28, y + 15, 49, 12)
    display.rectangle(x + 37, y + 8, 33, 10)

    display.set_pen(body)
    display.rectangle(x + 6, y + 25, 105, 13)
    display.rectangle(x + 30, y + 16, 44, 9)
    display.rectangle(x + 39, y + 9, 29, 7)
    display.rectangle(x + 72, y + 22, 32, 5)

    display.set_pen(body_light)
    display.rectangle(x + 10, y + 25, 22, 2)
    display.rectangle(x + 77, y + 23, 24, 2)

    display.set_pen(window)
    display.rectangle(x + 40, y + 11, 27, 4)
    display.rectangle(x + 33, y + 17, 17, 7)
    display.rectangle(x + 53, y + 17, 19, 7)

    display.set_pen(teal)
    display.rectangle(x + 106, y + 29, 8, 4)
    display.rectangle(x + 1, y + 29, 4, 4)
    display.rectangle(x + 13, y + 19, 7, 3)

    display.set_pen(amber)
    display.rectangle(x + 5, y + 29, 4, 4)


def draw_scene(x, frame):
    display.set_pen(sky)
    display.clear()

    display.set_pen(stars)
    for star_x, star_y in star_positions:
        display.rectangle(star_x, star_y, 2, 2)

    display.set_pen(horizon)
    display.rectangle(0, road_y - 4, width, 4)

    display.set_pen(road)
    display.rectangle(0, road_y, width, height - road_y)

    display.set_pen(road_line)
    offset = (frame * 4) % 54
    for line_x in range(-54 + offset, width, 54):
        display.rectangle(line_x, road_y + 17, 25, 2)

    display.set_pen(body_light)
    display.text("TIME-TRAVEL EXPRESS", 12, 12, width - 24, 1)

    draw_car(x, car_y)
    display.update()


frame = 0
while True:
    draw_scene(car_x, frame)
    car_x += 3
    if car_x > width:
        car_x = -car_width
    frame = (frame + 1) % 54
    time.sleep_ms(35)
