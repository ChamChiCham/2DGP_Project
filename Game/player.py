from pico2d import load_font, load_image
from define import *
import server
import game_framework

# class Player는 각각 독립된 객체가 아닌 모든 플레이어 정보를 관리한다.
class Player:
    def __init__(self, _count = 2):
        self.score = [0, 0, 0, 0]
        self.turn = 0
        self.count = _count
        self.font = load_font('ENCR10B.TTF', 30)
        self.image = []
        for i in range(_count):
            self.image.append(load_image('image\\player' + str(i + 1) + '.png'))
        pass

    def draw(self):
        for i in range(self.count):
            self.image[i].draw(WINDOW_WIDTH / 4 * i + WINDOW_WIDTH / 8 - 50, WINDOW_HEIGHT - 100, 100, 150)
            if self.turn == i:
                self.font.draw(WINDOW_WIDTH / 4 * i + WINDOW_WIDTH / 8 + 50, WINDOW_HEIGHT - 100, f'{self.score[i]}', (255, 155, 0))
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

    def add_score(self, _value):
        self.score[self.turn] += 10 * _value

        if self.score[self.turn] < 0:
            self.score[self.turn] = 0

        if self.score[self.turn] == server.target_score:
            import result_mode
            game_framework.push_mode(result_mode)


