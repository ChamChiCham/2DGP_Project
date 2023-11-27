# #####
# background.py: 배경 클래스가 구현되어 있는 파일.
# #####
from pico2d import load_image
from define import *

class PlayBackground:
    # 이미지 변수
    image_background = None
    image_board = None

    def __init__(self):
        if self.image_background == None:
            self.image_background = load_image('image\\background_playing.jpg')

        if self.image_board == None:
            self.image_board = load_image('image\\board.png')

    # draw(): 이미지 그리기
    def draw(self):
        self.image_background.draw(1280 // 2, 960 // 2)
        self.image_board.draw(1280 // 2 + 5, 960 // 2 - 2)

    # update():
    def update(self):
        pass

class TitleBackground:
    image_background = None

    def __init__(self):
        if self.image_background == None:
            self.image_background = load_image('image\\background_title.jpg')
            self.image_title = load_image('image\\title.png')
    pass

    def draw(self):
        self.image_background.draw_to_origin(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.image_title.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 200, TITLE_WIDTH, TITLE_HEIGHT)

    def update(self):
        pass
