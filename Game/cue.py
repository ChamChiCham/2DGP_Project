import math

from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

from define import *
import game_framework


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


class Ready:
    @staticmethod
    def enter(cue, e):
        if right_down(e) or left_up(e):
            cue.dir -= 1
        elif left_down(e) or right_up(e):
            cue.dir += 1
        pass

    @staticmethod
    def exit(cue, e):
        pass

    @staticmethod
    def do(cue):
        cue.degree += 0.5 * cue.dir
        if cue.degree >= 360.0:
            cue.degree -= 360.0

    @staticmethod
    def draw(cue):
        degree = math.radians(cue.degree)
        cue.image.clip_composite_draw(0, 0, CUE_WIDTH, CUE_HEIGHT, degree, '',
                                      cue.x + (CUE_WIDTH // 2 + BALL_SIZE) * math.cos(degree + math.pi),
                                      cue.y + (CUE_WIDTH // 2 + BALL_SIZE) * math.sin(degree + math.pi))




class StateMachine:
    def __init__(self, cue):
        self.cue = cue
        self.cur_state = Ready
        self.transitions = {
            Ready: {right_down: Ready, left_down: Ready, left_up: Ready, right_up: Ready}
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
        # cue가 가리키는 위치
        self.x, self.y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.dir = 0
        self.degree = 30
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.image = load_image('image_cue.png')
        pass

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    # def handle_collision(self, group, other):
    #     pass