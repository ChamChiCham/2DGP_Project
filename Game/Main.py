# #####
# Main.py: 게임 루프가 구현 되어 있는 메인 프로세스 파일
# #####
from pico2d import *
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
    # Init variable
    global running

    running = True

    # Create Object Here.

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
    game_world.render()
    update_canvas()

# ---
# Game Process: 게임 월드 내 모든 객체를 그린다.
# ---
open_canvas()
create_world()
# game loop
while running:
    time_started = get_time()
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()