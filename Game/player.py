from pico2d import load_font
from define import *


class Player:
    def __init__(self, _count = 2):
        self.score = [0, 0, 0, 0]
        self.turn = 0
        self.count = _count
        self.font = load_font('ENCR10B.TTF', 30)
        pass

    def draw(self):
        for i in range(self.count):
            if self.turn == i:
                self.font.draw(WINDOW_WIDTH / 4 * i + WINDOW_WIDTH / 8 + 50, WINDOW_HEIGHT - 100, f'{self.score[i]}', (0, 0, 255))
            else:
                self.font.draw(WINDOW_WIDTH / 4 * i + WINDOW_WIDTH / 8 + 50, WINDOW_HEIGHT - 100, f'{self.score[i]}', (255, 255, 255))
        pass

    def update(self):
        pass

    def get_bb(self):
        pass

    def next_turn(self):
        self.turn += 1
        if self.turn == self.count:
            self.turn = 0

