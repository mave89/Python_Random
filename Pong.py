# REQUIREMENT - Pygame - https://pypi.python.org/pypi/SimpleGUICS2Pygame

# Implementation of classic arcade game Pong
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

# Initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
#LEFT = False
#RIGHT = True

# Initialize ball_pos and ball_vel for new ball in middle of table
# If direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel 
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [(random.randrange(120, 240)) / 60, (random.randrange(60, 180)) / 60]
    
    if direction == "LEFT":
        ball_vel = [-ball_vel[0], -ball_vel[1]]
    elif direction == "RIGHT":
        ball_vel = [ball_vel[0], -ball_vel[1]]

# Define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(random.choice(["RIGHT","LEFT"]))
    #spawn_ball(a)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # Draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # Update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
            
    # Draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # Update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT and paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT and paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    # Draw paddles
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT],
                         [0, paddle1_pos + HALF_PAD_HEIGHT],
                         [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],
                         [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT]], 
                        1, 'Red', 'Red')
    
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT],
                         [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT],
                         [WIDTH, paddle2_pos + HALF_PAD_HEIGHT],
                         [WIDTH, paddle2_pos - HALF_PAD_HEIGHT]],
                        1, 'Red', 'Red')
    
    # Determine whether paddle and ball collide
    if (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS):
        if ball_pos[1] > paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - 1.1 * ball_vel[0]
        else:
            score2 += 1
            spawn_ball("RIGHT")
    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] > paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - 1.1 * ball_vel[0]
        else:
            score1 += 1
            spawn_ball("LEFT")
    
    # Draw scores
    canvas.draw_text(str(score1), (200, 60), 40, 'Yellow')
    canvas.draw_text(str(score2), (400, 60), 40, 'Yellow')
        
def keydown(key):
    a = 5
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= a
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += a
    
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= a
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += a
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# Button to restart game
def button_handler():
    new_game()

# Create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', button_handler, 50)


# Start frame
new_game()
frame.start()
