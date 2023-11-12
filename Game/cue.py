import math

from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE, SDLK_r

from define import *
import game_framework
import game_world
from ball import Ball


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE

def r_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r


# ---
# Ready: 공을 칠 준비를 하는 상태. 큐대의 방향을 조절한다.
# ---
class Ready:
    @staticmethod
    def enter(cue, e):
        if right_down(e) or left_up(e):
            cue.dir -= 1
        elif left_down(e) or right_up(e):
            cue.dir += 1
        elif space_down(e):
            cue.charging = True
        elif r_down(e):
            # 목표 공의 색 바꾸기
            if cue.target_color == BALL_COLOR_WHITE:
                cue.target_color = BALL_COLOR_YELLOW
            else:
                cue.target_color = BALL_COLOR_WHITE

            # 목표공의 위치로 큐대 이동
            for o in game_world.objects[1]:
                 if o.color == cue.target_color:
                     cue.x, cue.y = o.x + BOARD_X, o.y + BOARD_Y

    @staticmethod
    def exit(cue, e):
        pass

    @staticmethod
    def do(cue):
        cue.degree += 0.5 * cue.dir
        if cue.degree >= 360.0:
            cue.degree -= 360.0
        if cue.degree < 0.0:
            cue.degree += 360.0


    @staticmethod
    def draw(cue):
        degree = math.radians(cue.degree)
        cue.image.clip_composite_draw(0, 0, CUE_WIDTH, CUE_HEIGHT, degree, '',
                                      cue.x + (CUE_WIDTH // 2 + BALL_SIZE) * math.cos(degree + math.pi),
                                      cue.y + (CUE_WIDTH // 2 + BALL_SIZE) * math.sin(degree + math.pi))


# ---
# Wait: 공이 멈추기를 기다리는 상태.
# ---
class Wait:
    @staticmethod
    def enter(cue, e):
        print("Wait")
        for o in game_world.objects[1]:
             if o.color == cue.target_color:
                 o.velocity = cue.power / 4
                 o.degree = cue.degree

        pass

    @staticmethod
    def exit(cue, e):
        pass

    @staticmethod
    def do(cue):
        pass

    @staticmethod
    def draw(cue):
        pass

# ---
# Charge: 큐가 스페이스바를 눌러 충전중인 상태.
# ---
class Charge:
    @staticmethod
    def enter(cue, e):
        cue.power = 1.0
        pass

    @staticmethod
    def exit(cue, e):
        pass

    @staticmethod
    def do(cue):
        cue.power += 0.1
        if cue.power > 20.0:
            cue.power = 1.0
        pass

    @staticmethod
    def draw(cue):
        degree = math.radians(cue.degree)
        cue.image.clip_composite_draw(0, 0, CUE_WIDTH, CUE_HEIGHT, degree, '',
                                      cue.x + (CUE_WIDTH // 2 + BALL_SIZE + cue.power * 2) * math.cos(degree + math.pi),
                                      cue.y + (CUE_WIDTH // 2 + BALL_SIZE + cue.power * 2) * math.sin(degree + math.pi))
        pass


class StateMachine:
    def __init__(self, cue):
        self.cue = cue
        self.cur_state = Ready
        self.transitions = {
            Ready: {right_down: Ready, left_down: Ready, left_up: Ready, right_up: Ready, space_down: Charge},
            Charge: {space_up: Wait},
            Wait: {r_down: Ready}
        }

    def start(self):
        self.cur_state.enter(self.cue, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.cue)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.cue, e)
                self.cur_state = next_state
                self.cur_state.enter(self.cue, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.cue)


class Cue:

    def __init__(self):

        self.target_color = BALL_COLOR_WHITE

        # cue가 가리키는 위치
        for o in game_world.objects[1]:
             if o.color == self.target_color:
                 self.x, self.y = o.x + BOARD_X, o.y + BOARD_Y
        # 큐가 돌아가는 방향 설정
        self.dir = 0

        # 큐의 방향
        self.degree = 30
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.image = load_image('image_cue.png')
        self.power = 5.0
        pass

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        pass

