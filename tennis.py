from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
import machine
import time
import random
import os
import utime

# -----------------------------
# Display Setup
# -----------------------------
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)
WIDTH, HEIGHT = display.get_bounds()

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

# -----------------------------
# Buttons
# -----------------------------
button_a = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)  # up
button_b = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)  # down

# -----------------------------
# Game State
# -----------------------------
paddle_w = 5
paddle_h = 40

player_x = 0
player_y = HEIGHT // 2 - paddle_h // 2
player_speed = 10

ai_x = WIDTH - paddle_w
ai_y = HEIGHT // 2 - paddle_h // 2
ai_speed = 10  # difficulty

ball_size = 5
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = -10
ball_dy = 10

score1 = 0
score2 = 0
highscore = 0

frame_count = 0
start_time = utime.ticks_ms() # Use milliseconds for longer intervals

fps_s = "0"
fps=0

def circle_rectangle_collision(circle_x, circle_y, circle_radius, rect_x, rect_y, rect_width, rect_height):
    """
    Detects collision between an axis-aligned rectangle and a circle.
    The rectangle is defined by its top-left corner (rect_x, rect_y).
    """
    
    # Find the closest point on the rectangle to the center of the circle
    closest_x = max(rect_x, min(circle_x, rect_x + rect_width))
    closest_y = max(rect_y, min(circle_y, rect_y + rect_height))
    
    # Calculate the distance between the closest point and the circle's center
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y
    
    # Use the Pythagorean theorem to check if the distance is less than the radius
    distance_squared = (distance_x * distance_x) + (distance_y * distance_y)
    
    # Collision occurs if the distance is less than or equal to the radius
    return distance_squared <= (circle_radius * circle_radius)


# -----------------------------
# High Score Load/Save
# -----------------------------
def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_highscore(value):
    with open("highscore.txt", "w") as f:
        f.write(str(value))

highscore = load_highscore()

# -----------------------------
# Helpers
# -----------------------------
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-8, -9,-10,10,9,8])
    ball_dy = random.choice([-8, -9,-10,10,9,8])
    #ball_dx = -10
    #ball_dy = 10

def draw():
    
    display.set_pen(BLACK)
    display.clear()

    # Player paddle
    display.set_pen(WHITE)
    display.rectangle(player_x, player_y, paddle_w, paddle_h)
    
    #display.rectangle(100, 100, 20, 20)

    # AI paddle
    display.rectangle(ai_x, ai_y, paddle_w, paddle_h)

    # Ball
    display.circle(int(ball_x), int(ball_y), int(5))
    #display.rectangle(ball_x, ball_y, ball_size, ball_size)

    # Score
    display.text(f"Player 1: {score1}", 5, 5, scale=1.5)
    display.text(f"Player 2: {score2}", WIDTH - 80, 5, scale=1)
    display.text(f"High: {highscore}", 130, 5, scale=1)

    display.update()
    
def end_game_check():
    
    global score1
    global score2
    global highscore
    
    return
    
    if score1 > 11 or score2 > 11 :
                
        if score1 > highscore:
            highscore = score1      
        
        if score2 > highscore:
            highscore = score2
        
        save_highscore(highscore)
        
        score1 = 0
        score2 = 0
        return True
    else:
        return False
        
        

def game_over_flash():
    
    display.set_pen(BLACK)
    display.clear()
    
    display.set_pen(WHITE)
    display.text("GAME OVER", WIDTH//2 - 40, HEIGHT//2 - 10, scale=2)
    display.update()
    time.sleep(5)
    display.set_pen(BLACK)
    display.clear()

# -----------------------------
# Main Loop
# -----------------------------
while True:

    # -------------------------
    # Player movement
    # -------------------------
    if not button_a.value():
       player_y -= player_speed
    if not button_b.value():
       player_y += player_speed

    player_y = max(0, min(HEIGHT - paddle_h, player_y))

    # -------------------------
    # AI movement
    # -------------------------
    if ai_y + paddle_h/2 < ball_y:
        ai_y += ai_speed
    elif ai_y + paddle_h/2 > ball_y:
        ai_y -= ai_speed

    ai_y = max(0, min(HEIGHT - paddle_h, ai_y))

    # -------------------------
    # Ball movement
    # -------------------------
    print(f"Ball DX: {ball_dx:.2f}")
    print(f"Ball DY: {ball_dy:.2f}")
    print(f"Ball X: {ball_x:.2f}")
    print(f"Ball Y: {ball_y:.2f}")
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce top/bottom
    if ball_y <= 0 or ball_y + ball_size >= HEIGHT:
        ball_dy = -ball_dy

    # Player collision
    
    player_collision_detected  = circle_rectangle_collision(ball_x, ball_y, ball_size, player_x, player_y, paddle_w, paddle_h)
    ai_collision_detected  = circle_rectangle_collision(ball_x, ball_y, ball_size, ai_x, ai_y, paddle_w, paddle_h)

    #print(f"Ball X: {ball_dx:.2f}")
    #print(f"Ball Y: {ball_dy:.2f}")


   # print(f"Ball X: {ball_x:.2f}")
   # print(f"Ball Y: {ball_y:.2f}")
    #print(f"Player X: {player_x:.2f}")
    #print(f"Player Y: {player_y:.2f}")
    #print(f"Paddle X: {paddle_w:.2f}")
    #print(f"Paddle Y: {paddle_h:.2f}")

    if (player_collision_detected):
        #print(f"Player Collision detected: {player_collision_detected}")
        ball_dx = -ball_dx
        

    # AI collision    
    if (ai_collision_detected):
        print(f"AI Collision detected: {ai_collision_detected}")
        ball_dx = -ball_dx

    # -------------------------
    # Missed ball → Game Over
    # -------------------------
    if ball_x <= 0:
        
        if end_game_check():
            game_over_flash()            
        else:
            score2 += 1
        
        reset_ball()

        

    # Bounce off right wall if AI misses (rare)
    if ball_x + ball_size >= WIDTH:
        
        if end_game_check():
            game_over_flash()            
        else:
            score1 += 1
        
        reset_ball()

        
        score1 += 1
        reset_ball()

    frame_count += 1
    
    # Check if one second has passed
    
    if utime.ticks_diff(utime.ticks_ms(), start_time) >= 1000:
        elapsed_time = utime.ticks_diff(utime.ticks_ms(), start_time) / 1000.0
        fps = frame_count / elapsed_time
        #print(f"Average FPS: {fps:.2f}")
        fps_s = f"Average FPS: {fps:.2f}"
        
        # Reset counters
        frame_count = 0
        start_time = utime.ticks_ms()

   
    draw()
    #time.sleep(0.01)
