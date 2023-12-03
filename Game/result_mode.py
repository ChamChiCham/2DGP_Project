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
    music = load_music("game_win.mp3")
    music.set_volume(32)
    music.play()
    server.buttons.append(Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4, _str='TITLE', _act=Button.act_title))
    game_world.add_objects(server.buttons, 3)
    text = load_font('ENCR10B.TTF', TEXT_FONT_SIZE)
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    result = "PLAYER " + str(server.player.turn + 1) + " Win!"
    text.draw(WINDOW_WIDTH // 2 - TEXT_FONT_DIFF * len(result), WINDOW_HEIGHT // 8 * 5, result, (255, 0, 50))
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