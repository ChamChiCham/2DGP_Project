from pico2d import *

import game_framework
import game_world
import server
from define import *
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
    global text
    server.buttons.append(Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4, _str='TITLE', _act=Button.act_title))
    game_world.add_objects(server.buttons, 3)
    text = load_font('ENCR10B.TTF', TEXT_FONT_SIZE)
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    text.draw(WINDOW_WIDTH // 2 - TEXT_FONT_DIFF * 6, WINDOW_HEIGHT // 4 * 3, "RESULT", (255, 0, 0))
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