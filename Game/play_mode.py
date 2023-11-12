from pico2d import *
from define import *

import game_framework
import game_world


from ball import Ball
from background import Background
from cue import Cue

# ---
# handle_events(): 이벤트를 받고 각 객체에게 전달한다.
# ---
def handle_events():
    global running

    # Get events
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            cue.handle_event(event)


# ---
# init(): 객체와 변수들을 초기화한다.
# ---
def init():
    global cue
    global ball_targ

    # Init variable

    # Create Object Here.
    background = Background()
    game_world.add_object(background, 0)

    ball_red1 = Ball(_color=BALL_COLOR_RED)
    game_world.add_object(ball_red1, 1)

    ball_red2 = Ball(_color=BALL_COLOR_RED)
    game_world.add_object(ball_red2, 1)

    ball_white = Ball(300, 200, BALL_COLOR_WHITE)
    game_world.add_object(ball_white, 1)

    ball_yellow = Ball(BOARD_WIDTH, BOARD_HEIGHT, BALL_COLOR_YELLOW)
    game_world.add_object(ball_yellow, 1)

    ball_targ = ball_white

    cue = Cue()
    game_world.add_object(cue, 2)

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()

def draw():
    clear_canvas()
    # 객체 그리기
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

