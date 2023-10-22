# #####
# ball.py: 당구공이 구현되어 있는 파일.
# #####
from pico2d import load_image

class Ball:

    # 이미지 변수
    image_white_ball = None
    image_yellow_ball = None
    image_red_ball = None

    # 상태 변수
    # color: 공의 색상 / 0: White, 1: Yellow, 2: Red
    color = None
    # pos: "Board 위에서의" x, y 위치
    pos_x = pos_y = 0

    def __init__(self, _x = 800 // 2, _y = 400 // 2, _color = 0):
        # 이미지 로드
        if self.image_white_ball == None:
            self.image_white_ball = load_image('image_white_ball.png')

        if self.image_yellow_ball == None:
            self.image_yellow_ball = load_image('image_yellow_ball.png')

        if self.image_red_ball == None:
            self.image_red_ball = load_image('image_red_ball.png')

        # 상태값 대입
        self.color = _color
        self.pos_x = _x
        self.pos_y = _y

    # draw(): 이미지 그리기
    def draw(self):
        if self.color == 0:
            self.image_white_ball.clip_draw(0, 0, 100, 100, 240 + self.pos_x, 280 + self.pos_y, 17, 17)
        elif self.color == 1:
            self.image_yellow_ball.clip_draw(0, 0, 100, 100, 240 + self.pos_x, 280 + self.pos_y, 17, 17)
        elif self.color == 2:
            self.image_red_ball.clip_draw(0, 0, 100, 100, 240 + self.pos_x, 280 + self.pos_y, 17, 17)

    # update():
    def update(self):
        pass