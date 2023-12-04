from pico2d import load_image, load_font, load_music
from sdl2 import SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP
from sdl2.sdlmixer import music_finished

import game_framework
import game_world
from define import *
import server

class Button:
    image = None
    sound = None

    def __init__(self, _x = 250, _y = 400, _str = 'NONE', _act = None, _arg = None):
        if self.image == None:
            self.image = load_image('image\\button.png')
            self.font = load_font('ENCR10B.TTF', BUTTON_FONT_SIZE)
        self.x = _x
        self.y = _y
        self.str = _str
        self.act = _act
        self.arg = _arg
        if not self.sound:
            self.sound = load_music("sound\\button_blop.mp3")
            self.sound.set_volume(32)
    pass

    def draw(self):
        self.image.draw(self.x, self.y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.font.draw(self.x - (len(self.str) * BUTTON_FONT_DIFF), self.y, self.str, (255, 255, 255))

    def update(self):
        pass

    def get_bb(self):
        return (self.x - BUTTON_WIDTH // 2, self.y - BUTTON_HEIGHT // 2,
                self.x + BUTTON_WIDTH // 2, self.y + BUTTON_HEIGHT // 2)

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, WINDOW_HEIGHT - 1 - event.y
            bb = self.get_bb()
            if bb[0] <= x <= bb[2] and bb[1] <= y <= bb[3] and self.act != None:
                self.sound.play()
        elif event.type == SDL_MOUSEBUTTONUP:
            x, y = event.x, WINDOW_HEIGHT - 1 - event.y
            bb = self.get_bb()
            if bb[0] <= x <= bb[2] and bb[1] <= y <= bb[3] and self.act != None:
                self.act(self.arg) if self.arg != None else self.act()

    # callback function for Button.act
    @staticmethod
    def act_quit():
        game_framework.quit()

    @staticmethod
    def act_play():
        Button.clear_buttons()
        server.buttons.append(Button(BUTTON_POSITION_TITLE_X, BUTTON_POSITION_TITLE_Y * 4, '2 PLAYER', Button.act_set_player, 2))
        server.buttons.append(Button(BUTTON_POSITION_TITLE_X, BUTTON_POSITION_TITLE_Y * 3, '3 PLAYER', Button.act_set_player, 3))
        server.buttons.append(Button(BUTTON_POSITION_TITLE_X, BUTTON_POSITION_TITLE_Y * 2, '4 PLAYER', Button.act_set_player, 4))
        server.buttons.append(Button(BUTTON_POSITION_TITLE_X, BUTTON_POSITION_TITLE_Y * 1, 'BACK', Button.act_back_to_title))
        game_world.add_objects(server.buttons, 1)

    @staticmethod
    def act_set_player(_count):
        server.player_count = _count
        Button.clear_buttons()
        server.buttons.append(
            Button(BUTTON_POSITION_TITLE_X, BUTTON_POSITION_TITLE_Y * 4, str(BUTTON_SCORE_FIR), Button.act_set_score, BUTTON_SCORE_FIR))
        server.buttons.append(
            Button(BUTTON_POSITION_TITLE_X, BUTTON_POSITION_TITLE_Y * 3, str(BUTTON_SCORE_SEC), Button.act_set_score, BUTTON_SCORE_SEC))
        server.buttons.append(
            Button(BUTTON_POSITION_TITLE_X, BUTTON_POSITION_TITLE_Y * 2, str(BUTTON_SCORE_THI), Button.act_set_score, BUTTON_SCORE_THI))
        server.buttons.append(
            Button(BUTTON_POSITION_TITLE_X, BUTTON_POSITION_TITLE_Y * 1, 'BACK', Button.act_play))
        game_world.add_objects(server.buttons, 1)

    @staticmethod
    def act_set_score(_score):
        server.target_score = _score
        import play_mode
        game_framework.change_mode(play_mode)


    @staticmethod
    def act_back_to_title():
        Button.clear_buttons()
        server.buttons.append(Button(BUTTON_POSITION_TITLE_X, BUTTON_POSITION_TITLE_Y * 2, 'PLAY', Button.act_play))
        server.buttons.append(Button(BUTTON_POSITION_TITLE_X, BUTTON_POSITION_TITLE_Y * 1, 'QUIT', Button.act_quit))
        game_world.add_objects(server.buttons, 1)

    @staticmethod
    def act_back_to_play():
        Button.clear_buttons()
        game_framework.pop_mode()

    @staticmethod
    def act_title():
        import title_mode
        game_framework.pop_mode()
        game_framework.change_mode(title_mode)

    @staticmethod
    def clear_buttons():
        for button in server.buttons:
            game_world.remove_object(button)
        server.buttons.clear()


