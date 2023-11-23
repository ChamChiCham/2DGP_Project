from pico2d import clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_world
import game_framework
from Game.button import Button
from background import TitleBackground as Background


def handle_events():
    # Get events
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            pass
    pass


def init():
    background = Background()
    game_world.add_object(background, 0)

    buttons = []
    buttons.append(Button(250, 300, 'PLAY'))
    buttons.append(Button(250, 150, 'QUIT'))

    for button in buttons:
        game_world.add_object(button, 1)


    pass


def finish():
    game_world.clear()
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