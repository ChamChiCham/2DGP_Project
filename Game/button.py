from pico2d import load_image, load_font
from sdl2 import SDL_MOUSEBUTTONDOWN

from define import *

class Button:
    image = None

    def __init__(self, _x = 250, _y = 400, _str = 'NONE', _act = None):
        if self.image == None:
            self.image = load_image('image_button.png')
            self.font = load_font('ENCR10B.TTF', BUTTON_FONT_SIZE)
            self.x = _x
            self.y = _y
            self.str = _str
            self.act = _act
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
                self.act()
        pass

    # callback function for Button.act
    @staticmethod
    def act_print():
        print('print')
