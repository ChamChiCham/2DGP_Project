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

    # Init variable

    # Create Object Here.
    background = Background()
    game_world.add_object(background, 0)

    balls = []
    balls.append(Ball(150, 200, BALL_COLOR_RED))
    balls.append(Ball(550, 200, BALL_COLOR_RED))
    balls.append(Ball(75, 200, BALL_COLOR_WHITE))
    balls.append(Ball(550, 230, BALL_COLOR_YELLOW))

    for ball in balls:
        game_world.add_object(ball, 1)
        game_world.add_collision_pair('ball:ball', ball, ball)

    cue = Cue()
    game_world.add_object(cue, 2)

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collision()

def draw():
    clear_canvas()
    # 객체 그리기
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

