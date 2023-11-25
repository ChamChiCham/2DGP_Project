from pico2d import *

import game_framework
import game_world
import server
from button import Button
from copy import copy



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            for button in copy(server.buttons):
                button.handle_event(event)


def init():
    server.buttons.append(Button(_str='TEST', _act=Button.act_quit))
    game_world.add_objects(server.buttons, 3)

    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    for button in server.buttons:
        game_world.remove_object(button)
    server.buttons.clear()
    pass

def pause():
    pass

def resume():
    pass