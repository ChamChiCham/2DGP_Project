# #####
# define.py: 전역 상수가 저장되어 있는 파일.
# #####

# ---
# 상수 정의
# ---
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 960
WINDOW_FRAME = 1.0 / 60.0

BOARD_WIDTH, BOARD_HEIGHT = 800, 400

BALL_SIZE = 18
BALL_COLOR_WHITE, BALL_COLOR_YELLOW, BALL_COLOR_RED = 0, 1, 2
BALL_ACCEL = -100

CUE_WIDTH, CUE_HEIGHT = 337, 21

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
