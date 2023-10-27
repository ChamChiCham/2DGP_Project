# #####
# background.py: 배경 클래스가 구현되어 있는 파일.
# #####
from pico2d import load_image

class Background:

    # 이미지 변수
    image_background = None
    image_board = None

    def __init__(self):
        if self.image_background == None:
            self.image_background = load_image('image_background_playing.jpg')

        if self.image_board == None:
            self.image_board = load_image('image_board.png')

    # draw(): 이미지 그리기
    def draw(self):
        self.image_background.draw(1280 // 2, 960 // 2)
        self.image_board.draw(1280 // 2 + 5, 960 // 2 - 2)

    # update():
    def update(self):
        pass