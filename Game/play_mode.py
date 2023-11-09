from pico2d import *
from define import *

import game_framework
import game_world

from ball import Ball
from background import Background

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


# ---
# init(): 객체와 변수들을 초기화한다.
# ---
def init():
    global background

    # Init variable

    # Create Object Here.
    background = Background()
    game_world.add_object(background, 0)

    ball = Ball()
    game_world.add_object(ball, 1)

    ball = Ball(300, 200, 1)
    ball.set_value(1000, 65)
    game_world.add_object(ball, 1)

    ball = Ball(BOARD_WIDTH, BOARD_HEIGHT, 2)
    game_world.add_object(ball, 1)

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