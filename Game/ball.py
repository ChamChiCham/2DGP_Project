# #####
# ball.py: 당구공이 구현되어 있는 파일.
# #####
import math
from pico2d import load_image, draw_rectangle
from define import *
import game_framework
import server

class Ball:

    # 이미지 변수
    image = None

    # 상태 변수
    # color: 공의 색상
    color = None

    # pos: "Board 위에서의" x, y 위치 / 자료형: float
    x = y = None

    # degree: 공이 향하는 방향의 각도 / 단위: (0 - 2ㅠ) 라디안
    angle = 0

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

        self.collide = False

    # draw(): 이미지 그리기
    def draw(self):
        self.image.clip_draw(0, 0, 100, 100, BOARD_X + int(self.x), BOARD_Y + int(self.y), BALL_SIZE + 1, BALL_SIZE + 1)
        # draw_rectangle(*self.get_bb())


    # update()
    def update(self):
        # 공의 이동
        if self.velocity > 0:
            r = self.velocity * game_framework.frame_time + 0.5 * pow(game_framework.frame_time, 2) * BALL_ACCEL
            self.x += r * math.cos(self.angle) * METER_PER_PIXEL
            self.y += r * math.sin(self.angle) * METER_PER_PIXEL
            self.velocity += BALL_ACCEL * game_framework.frame_time

            # 단위를 라디안에서 도로 변경
            degree = math.degrees(self.angle)
            while degree < 0:
                degree += 360
            while degree > 360:
                degree -= 360

            # 공이 왼쪽 면에 닿았을 때
            if self.x >= BOARD_WIDTH:
                # 방향 전환
                if degree > 270 and not 90 <= degree <= 180:
                    degree -= 2 * (degree - 270)
                else:
                    degree += 2 * (90 - degree)

                self.x -= (self.x - BOARD_WIDTH) * 2

            # 공이 오른쪽 면에 닿았을 때
            elif self.x <= 0 and 90 < degree < 270:
                # 방향 전환
                if degree < 180:
                    degree -= 2 * (degree - 90)
                else:
                    degree += 2 * (270 - degree)

                self.x = -self.x

            # 공이 위쪽 면에 닿았을 때
            elif self.y >= BOARD_HEIGHT and 0 < degree < 180:
                # 방향 전환
                degree += 2 * (180 - degree)

                self.y -= (self.y - BOARD_HEIGHT) * 2

            # 공이 아래쪽 면에 닿았을 때
            elif self.y <= 0 and 180 < degree < 360:
                # 방향 전환
                degree += 2 * (180 - degree)

                self.y = -self.y

            self.angle = math.radians(degree)
        else:
            self.velocity = 0

    def get_bb(self):
        return (self.x - BALL_SIZE / 2 + BOARD_X, self.y - BALL_SIZE / 2 + BOARD_Y,
                self.x + BALL_SIZE / 2 + BOARD_X, self.y + BALL_SIZE / 2 + BOARD_Y)

    def handle_collision(self, group, other):
        if group == 'ball:ball' and self != other and self.velocity < other.velocity:
            # print(f"collision 'ball:ball' {self.color} / {other.color}")
            if BALL_SIZE > math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2):
                self.calc_collision(other)
                if self.color == server.cue.target_color and other.color == BALL_COLOR_RED:
                    other.collide = True
                elif self.color == BALL_COLOR_RED and other.color == server.cue.target_color:
                    self.collide = True

        pass

    def calc_collision(self, other):

        # 벡터를 더하는 과정
        if self.velocity > 0:
            vector_self = [self.velocity * math.cos(self.angle), self.velocity * math.sin(self.angle)]
            vector_other = [other.velocity * math.cos(other.angle), other.velocity * math.sin(other.angle)]
            vector_new = [vector_self[0] + vector_other[0], vector_self[1] + vector_other[1]]
            other.velocity = math.sqrt(vector_new[0]**2 + vector_new[1]**2)
            if vector_new[0] == 0:
                other.angle = math.pi / 2 if vector_new[1] > 0 else -math.pi / 2
            else:
                other.angle = math.atan(vector_new[1] / vector_new[0])
            self.velocity = 0

        # 각도 저장
        angle = other.angle
        print(f"{math.degrees(self.angle)}, {math.degrees(other.angle)}, {math.degrees(angle)}")

        # 뒤로 이동
        self.calc_collision_move_back(other)

        # 각도 계산
        self.calc_collision_angle(other)

        # 속도 계산
        self_angle_diff = self.calc_collision_angle_difference(angle, self.angle)
        other_angle_diff = self.calc_collision_angle_difference(angle, other.angle)
            
        self.velocity = (1 - (self_angle_diff / (math.pi / 2))) * other.velocity
        other.velocity *= (1 - (other_angle_diff / (math.pi / 2)))

        # 앞으로 이동 (중복 충돌 방지)
        if self.velocity < other.velocity:
            while BALL_SIZE > math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2):
                other.x += 0.01 * math.cos(other.angle)
                other.y += 0.01 * math.sin(other.angle)
        else:
            while BALL_SIZE > math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2):
                self.x += 0.01 * math.cos(self.angle)
                self.y += 0.01 * math.sin(self.angle)
        print(f"{math.degrees(self.angle)}, {math.degrees(other.angle)}, {math.degrees(angle)}")


    def calc_collision_move_back(self, other):
        diff_square = (other.x - self.x)**2 + (other.y - self.y)**2
        dist = 1
        if BALL_SIZE**2 - diff_square > 0:
            dist = math.sqrt(BALL_SIZE**2 - diff_square)
            other.x += dist * math.cos(other.angle + math.pi)
            other.y += dist * math.sin(other.angle + math.pi)


    def calc_collision_angle(self, other):
        dx = self.x - other.x
        dy = self.y - other.y

        if dx != 0:
            angle = math.atan2(dy, dx)
        else:
            if dy > 0:
                angle = 0
            else:
                angle = math.pi 

        self.angle = angle

        self.angle = self.angle % (2 * math.pi)
        other.angle = other.angle % (2 * math.pi)

        angle_diff = self.angle - other.angle
        if 0 < angle_diff <= math.pi or angle_diff <= 0:
            other.angle = angle - math.pi / 2
        else:
            other.angle = angle + math.pi / 2
    
    def calc_collision_angle_difference(self, angle1, angle2):
        angle1 = angle1 % (2 * math.pi)
        angle2 = angle2 % (2 * math.pi)

        diff = abs(angle1 - angle2)

        if diff > math.pi:
            diff = 2 * math.pi - diff

        return diff











