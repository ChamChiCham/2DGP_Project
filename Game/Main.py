# #####
# Main.py: 게임 루프가 구현 되어 있는 메인 프로세스 파일
# #####
from pico2d import *
from define import *

import game_framework
import title_mode as start_mode

open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
game_framework.run(start_mode)
close_canvas()