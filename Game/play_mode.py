from pico2d import *

from Game.player import Player
from define import *

import game_framework
import game_world
import title_mode
import server


from ball import Ball
from background import PlayBackground as Background
from cue import Cue

def handle_events():
    # Get events
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            server.cue.handle_event(event)


def init():

    # Init variable

    # Create Object Here.
    background = Background()
    game_world.add_object(background, 0)

    # balls.append(Ball(150, 200, BALL_COLOR_RED))
    # balls.append(Ball(550, 200, BALL_COLOR_RED))
    # balls.append(Ball(75, 200, BALL_COLOR_WHITE))
    # balls.append(Ball(550, 230, BALL_COLOR_YELLOW))

    server.balls.append(Ball(520, 200, BALL_COLOR_RED))
    server.balls.append(Ball(550, 200, BALL_COLOR_RED))
    server.balls.append(Ball(75, 200, BALL_COLOR_WHITE))
    server.balls.append(Ball(550, 230, BALL_COLOR_YELLOW))

    for ball in server.balls:
        game_world.add_object(ball, 1)
        game_world.add_collision_pair('ball:ball', ball, ball)

    server.cue = Cue()
    game_world.add_object(server.cue, 2)

    server.player = Player(server.player_count)
    game_world.add_object(server.player,2)



def finish():
    game_world.clear()
    server.clear()
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

