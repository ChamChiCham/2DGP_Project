# #####
# ball.py: 당구공이 구현되어 있는 파일.
# #####
import math
from pico2d import load_image
from define import *

class Ball:

    # 이미지 변수
    image = None

    # 상태 변수
    # color: 공의 색상
    color = None

    # pos: "Board 위에서의" x, y 위치 / 자료형: float
    pos_x = pos_y = None

    # dir: 공의 방향 / 단위: 도
    dir = 0

    # velocity: px/s
    velocity = 0

    def __init__(self, _x = BOARD_WIDTH // 2, _y = BOARD_HEIGHT // 2, _color = BALL_COLOR_WHITE):
        # 이미지 로드
        if self.image == None:
            if _color == BALL_COLOR_WHITE:
                self.image = load_image('image_white_ball.png')
            elif _color == BALL_COLOR_YELLOW:
                self.image = load_image('image_yellow_ball.png')
            elif _color == BALL_COLOR_RED:
                self.image = load_image('image_red_ball.png')

        # 상태값 대입
        self.color = _color

        # max size: 800x400
        self.pos_x = float(_x)
        self.pos_y = float(_y)

    # draw(): 이미지 그리기
    def draw(self):
        self.image.clip_draw(0, 0, 100, 100, 240 + int(self.pos_x), 280 + int(self.pos_y), BALL_SIZE, BALL_SIZE)


    # update()
    def update(self):
        # 공의 이동
        if self.velocity != 0:
            r = self.velocity * WINDOW_FRAME + 0.5 * pow(WINDOW_FRAME, 2) * BALL_ACCEL
            self.pos_x += r * math.cos(math.radians(self.dir))
            self.pos_y += r * math.sin(math.radians(self.dir))
            self.velocity += BALL_ACCEL * WINDOW_FRAME

    def set_value(self, _velocity = 0, _dir = 0):
        self.velocity = _velocity
        self.dir = _dir