# #####
# Main.py: 게임 루프가 구현 되어 있는 메인 프로세스 파일
# #####
from pico2d import *
from background import Background
from ball import Ball
from define import *
import game_world

# ---
# handle_events(): 이벤트를 받고 각 객체에게 전달한다.
# ---
def handle_events():
    global running

    # Get events
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

# ---
# create_world(): 객체와 변수들을 초기화한다.
# ---
def create_world():
    global running
    global background

    # Init variable
    running = True

    # Create Object Here.
    background = Background()
    game_world.add_object(background, 0)

    ball = Ball()
    game_world.add_object(ball, 1)

    ball = Ball(0, 0, 1)
    game_world.add_object(ball, 1)

    ball = Ball(BOARD_WIDTH, BOARD_HEIGHT, 2)
    game_world.add_object(ball, 1)


# ---
# update_world(): 게임 월드 내 모든 객체를 업데이트한다.
# ---
def update_world():
    game_world.update()

# ---
# render_world(): 게임 월드 내 모든 객체를 그린다.
# ---
def render_world():
    clear_canvas()
    # 객체 그리기
    game_world.render()
    update_canvas()

# ---
# Game Process: 게임 월드 내 모든 객체를 그린다.
# ---
open_canvas()
create_world()
resize_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)

# game loop
while running:
    time_started = get_time()
    handle_events()
    update_world()
    render_world()
    time_elapsed = get_time() - time_started
    if time_elapsed > WINDOW_FRAME:
        time_elapsed = WINDOW_FRAME
    delay(WINDOW_FRAME - time_elapsed)

close_canvas()