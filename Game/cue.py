import math

from pico2d import load_image, load_music
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE, SDLK_r, SDL_MOUSEBUTTONUP, \
    SDL_MOUSEBUTTONDOWN, SDL_MOUSEMOTION

from define import *
import game_framework
import game_world
import server


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

def mouse_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONUP

def mouse_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN

def mouse_move(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEMOTION

def ball_stop(e):
    return e[0] == 'BALL_STOP'


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
        elif mouse_down(e):
            cue.mouse = True
        elif mouse_up(e):
            cue.mouse = False
        elif mouse_move(e) and cue.mouse:
            x, y = e[1].x, WINDOW_HEIGHT - 1 - e[1].y
            cue.angle = math.atan2(y - cue.y, x - cue.x)

        elif r_down(e) or ball_stop(e):
            # 목표 공의 색 바꾸기
            if cue.target_color == BALL_COLOR_WHITE:
                cue.target_color = BALL_COLOR_YELLOW
            else:
                cue.target_color = BALL_COLOR_WHITE

            # 목표공의 위치로 큐대 이동
            for ball in server.balls:
                 if ball.color == cue.target_color:
                     cue.x, cue.y = ball.x + BOARD_X, ball.y + BOARD_Y

            # 충돌상황에 따라 점수 부여 전달
            check = 1
            for ball in server.balls:
                 if ball.color == BALL_COLOR_RED and ball.collide == False:
                     check -= 1
                 if ball.color == BALL_COLOR_YELLOW and ball.collide == True:
                     check = -1
            if check:
                server.player.add_score(check)

            # 공의 충돌상황을 초기화
            for o in game_world.objects[1]:
                o.collide = False

            # player에 턴 바꾸기
            server.player.next_turn()

    @staticmethod
    def exit(cue, e):
        pass

    @staticmethod
    def do(cue):
        cue.angle += math.pi / 2 * cue.dir * game_framework.frame_time


    @staticmethod
    def draw(cue):
        cue.image.clip_composite_draw(0, 0, CUE_WIDTH, CUE_HEIGHT, cue.angle, '',
                                      cue.x + (CUE_WIDTH // 2 + BALL_SIZE) * math.cos(cue.angle + math.pi),
                                      cue.y + (CUE_WIDTH // 2 + BALL_SIZE) * math.sin(cue.angle + math.pi))


# ---
# Wait: 공이 멈추기를 기다리는 상태.
# ---
class Wait:
    @staticmethod
    def enter(cue, e):
        cue.sound_charge.stop()
        cue.sound_hit.play()
        for ball in server.balls:
             if ball.color == cue.target_color:
                 ball.velocity = cue.power / 4
                 ball.angle = cue.angle

        pass

    @staticmethod
    def exit(cue, e):
        pass

    @staticmethod
    def do(cue):
        check = True
        for o in game_world.objects[1]:
            if o.velocity > 0:
                check = False
                break
        if check:
            cue.state_machine.handle_event(('BALL_STOP', 0))


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
        cue.dir = 0
        cue.sound_charge.repeat_play()
        pass

    @staticmethod
    def exit(cue, e):
        pass

    @staticmethod
    def do(cue):
        cue.power += 10 * game_framework.frame_time
        if cue.power > 21.0:
            cue.power = 1.0
        pass

    @staticmethod
    def draw(cue):
        cue.image.clip_composite_draw(0, 0, CUE_WIDTH, CUE_HEIGHT, cue.angle, '',
                                      cue.x + (CUE_WIDTH // 2 + BALL_SIZE + cue.power * 2) * math.cos(cue.angle + math.pi),
                                      cue.y + (CUE_WIDTH // 2 + BALL_SIZE + cue.power * 2) * math.sin(cue.angle + math.pi))
        pass


class StateMachine:
    def __init__(self, cue):
        self.cue = cue
        self.cur_state = Ready
        self.transitions = {
            Ready: {right_down: Ready, left_down: Ready, left_up: Ready, right_up: Ready,
                    space_down: Charge, mouse_down: Ready, mouse_up: Ready, mouse_move: Ready},
            Charge: {space_up: Wait},
            Wait: {r_down: Ready, ball_stop: Ready}
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
        self.angle = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.image = load_image('image\\cue.png')
        self.power = 1.0
        self.mouse = False
        self.sound_charge = load_music("sound\\cue_charge.mp3")
        self.sound_charge.set_volume(32)
        self.sound_hit = load_music("sound\\ball_hit.mp3")
        self.sound_hit.set_volume(32)

        pass

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass

