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
    x = y = None

    # degree: 공이 향하는 방향의 각도 / 단위: (0 - 360)도
    degree = 0

    # velocity: px/s
    velocity = 0

    # 중심이 되는 공
    target = None

    def __init__(self, _x = BOARD_WIDTH // 2, _y = BOARD_HEIGHT // 2, _color = BALL_COLOR_WHITE, _target = False):
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
        self.x = float(_x)
        self.y = float(_y)

        self.target = _target

    # draw(): 이미지 그리기
    def draw(self):
        self.image.clip_draw(0, 0, 100, 100, BOARD_X + int(self.x), BOARD_Y + int(self.y), BALL_SIZE, BALL_SIZE)


    # update()
    def update(self):
        # 공의 이동
        if self.velocity > 0:
            r = self.velocity * WINDOW_FRAME + 0.5 * pow(WINDOW_FRAME, 2) * BALL_ACCEL
            self.x += r * math.cos(math.radians(self.degree))
            self.y += r * math.sin(math.radians(self.degree))
            self.velocity += BALL_ACCEL * WINDOW_FRAME

            # 공이 왼쪽 면에 닿았을 때
            if self.x >= BOARD_WIDTH:
                # 방향 전환
                if self.degree > 270 and not 90 <= self.degree <= 180:
                    self.degree -= 2 * (self.degree - 270)
                else:
                    self.degree += 2 * (90 - self.degree)

            # 공이 오른쪽 면에 닿았을 때
            elif self.x <= 0 and 90 < self.degree < 270:
                # 방향 전환
                if self.degree < 180:
                    self.degree -= 2 * (self.degree - 90)
                else:
                    self.degree += 2 * (270 - self.degree)

            # 공이 위쪽 면에 닿았을 때
            elif self.y >= BOARD_HEIGHT and 0 < self.degree < 180:
                # 방향 전환
                self.degree += 2 * (180 - self.degree)

            # 공이 아래쪽 면에 닿았을 때
            elif self.y <= 0 and 180 < self.degree < 360:
                # 방향 전환
                self.degree += 2 * (180 - self.degree)

    def set_value(self, _velocity = 0, _degree = 0):
        self.velocity = _velocity
        self.degree = _degree

    def get_bb(self):
        return self.x - BALL_SIZE / 2, self.y - BALL_SIZE / 2, self.x + BALL_SIZE / 2, self.y + BALL_SIZE / 2

    def handle_collision(self, group, other):
        pass


