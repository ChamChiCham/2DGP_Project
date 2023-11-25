from pico2d import load_font
from define import *
import server
import game_framework
import pause_mode

# class Player는 각각 독립된 객체가 아닌 모든 플레이어 정보를 관리한다.
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

    def add_score(self):
        self.score[self.turn] += 10
        if self.score[self.turn] == server.target_score:
            game_framework.push_mode(pause_mode)


