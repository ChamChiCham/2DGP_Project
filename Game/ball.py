# #####
# ball.py: 당구공이 구현되어 있는 파일.
# #####
import math
from pico2d import load_image, draw_rectangle
from define import *
import game_framework

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

    # velocity: m/s
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
        self.x = float(_x)
        self.y = float(_y)

    # draw(): 이미지 그리기
    def draw(self):
        self.image.clip_draw(0, 0, 100, 100, BOARD_X + int(self.x), BOARD_Y + int(self.y), BALL_SIZE, BALL_SIZE)
        # draw_rectangle(*self.get_bb())


    # update()
    def update(self):
        # 공의 이동
        if self.velocity > 0:
            r = self.velocity * game_framework.frame_time + 0.5 * pow(game_framework.frame_time, 2) * BALL_ACCEL
            self.x += r * math.cos(math.radians(self.degree)) * METER_PER_PIXEL
            self.y += r * math.sin(math.radians(self.degree)) * METER_PER_PIXEL
            self.velocity += BALL_ACCEL * game_framework.frame_time

            # 공이 왼쪽 면에 닿았을 때
            if self.x >= BOARD_WIDTH:
                # 방향 전환
                if self.degree > 270 and not 90 <= self.degree <= 180:
                    self.degree -= 2 * (self.degree - 270)
                else:
                    self.degree += 2 * (90 - self.degree)

                self.x -= (self.x - BOARD_WIDTH) * 2

            # 공이 오른쪽 면에 닿았을 때
            elif self.x <= 0 and 90 < self.degree < 270:
                # 방향 전환
                if self.degree < 180:
                    self.degree -= 2 * (self.degree - 90)
                else:
                    self.degree += 2 * (270 - self.degree)

                self.x = -self.x

            # 공이 위쪽 면에 닿았을 때
            elif self.y >= BOARD_HEIGHT and 0 < self.degree < 180:
                # 방향 전환
                self.degree += 2 * (180 - self.degree)

                self.y -= (self.y - BOARD_HEIGHT) * 2

            # 공이 아래쪽 면에 닿았을 때
            elif self.y <= 0 and 180 < self.degree < 360:
                # 방향 전환
                self.degree += 2 * (180 - self.degree)

                self.y = -self.y

    def set_value(self, _velocity = 0, _degree = 0):
        self.velocity = _velocity
        self.degree = _degree

    def get_bb(self):
        return (self.x - BALL_SIZE / 2 + BOARD_X, self.y - BALL_SIZE / 2 + BOARD_Y,
                self.x + BALL_SIZE / 2 + BOARD_X, self.y + BALL_SIZE / 2 + BOARD_Y)

    def handle_collision(self, group, other):
        if group == 'ball:ball' and self != other and self.velocity < other.velocity:
            # print(f"collision 'ball:ball' {self.color} / {other.color}")
            if BALL_SIZE * 2 > math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2):
                self.calc_collision(other)
        pass

    def calc_collision(self, other):
        # 공이 서로 이동 중일 때는 서로 방향을 바꾼다.
        dx = self.x - other.x
        dy = self.y - other.y

        if self.velocity > 0:
            self.degree = math.degrees(math.atan2(dy, dx))
            other.degree = math.degrees(math.atan2(-dy, -dx))

        # 한쪽 공만 이동 중일 때
        else:
            angle = math.atan2(dy, dx)
            angle1 = math.radians(other.degree)
            angle2 = angle + math.pi

            v1i = other.velocity
            v2i = self.velocity

            other.velocity = (0.8 * (v2i * math.cos(angle2 - angle) - v1i * math.cos(angle1 - angle)) + v1i * math.cos(angle1 - angle) + v1i * math.cos(angle1 - angle)) / 2
            self.velocity = (0.8 * (v1i * math.cos(angle1 - angle) - v2i * math.cos(angle2 - angle)) + v2i * math.cos(angle2 - angle) + v2i * math.cos(angle2 - angle)) / 2

            other.degree = math.degrees(angle1 + angle)
            other.degree = math.degrees(angle2 + angle)

            diff = BALL_SIZE * 2 - math.sqrt(dx**2 + dy**2)

            other.x += diff * math.cos(math.radians(other.degree))
            other.y += diff * math.sin(math.radians(other.degree))

            while other.degree >= 360.0:
                other.degree -= 360.0
            while other.degree < 0.0:
                other.degree += 360.0

            while self.degree >= 360.0:
                self.degree -= 360.0
            while self.degree < 0.0:
                self.degree += 360.0









