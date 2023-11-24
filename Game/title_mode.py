from pico2d import clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT

import game_world
import game_framework
from button import Button
from background import TitleBackground as Background
from define import *
import server
from copy import copy

def handle_events():
    # Get events
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            for button in copy(server.buttons):
                button.handle_event(event)

    pass


def init():
    background = Background()
    game_world.add_object(background, 0)

    Button.act_back()


def finish():
    game_world.clear()
    server.clear()
    pass


def update():
    game_world.update()
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass