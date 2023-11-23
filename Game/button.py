from pico2d import load_image, load_font

from define import *

class Button:
    image = None

    def __init__(self, _x = 250, _y = 400):
        if self.image == None:
            self.image = load_image('image_button.png')
            self.font = load_font('ENCR10B.TTF', 30)
            self.x = _x
            self.y = _y
            self.str = 'DISTANCE'
    pass

    def draw(self):
        self.image.draw(self.x, self.y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.font.draw(self.x - (len(self.str) * 9.5), self.y, self.str, (255, 255, 255))

    def update(self):
        pass