import math

from pico2d import load_image

from define import *
import game_framework

class Ready:
    @staticmethod
    def enter(cue, e):
        pass

    @staticmethod
    def exit(cue, e):
        pass

    @staticmethod
    def do(cue):
        pass

    @staticmethod
    def draw(cue):
        tdir = math.radians(cue.dir)
        cue.image.clip_composite_draw(0, 0, CUE_WIDTH, CUE_HEIGHT, tdir, '',
                                      cue.x + (CUE_WIDTH // 2 + BALL_SIZE) * math.cos(tdir + math.pi),
                                      cue.y + (CUE_WIDTH // 2 + BALL_SIZE) * math.sin(tdir + math.pi))




class StateMachine:
    def __init__(self, cue):
        self.cue = cue
        self.cur_state = Ready
        self.transitions = {
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
        self.dir = 30
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