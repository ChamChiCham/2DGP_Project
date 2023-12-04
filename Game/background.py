# #####
# background.py: 배경 클래스가 구현되어 있는 파일.
# #####
from pico2d import load_image, load_music
from define import *
import server

class PlayBackground:
    # 이미지 변수
    image_background = None
    image_board = None
    music = None

    def __init__(self):
        if not self.image_background:
            self.image_background = load_image('image\\background_playing.jpg')

        if not self.image_board:
            self.image_board = load_image('image\\board.png')

        if not self.music:
            self.music = load_music("sound\\background_play.mp3")
            self.music.set_volume(32)

        self.music.repeat_play()

    # draw(): 이미지 그리기
    def draw(self):
        self.image_background.draw(1280 // 2, 960 // 2)
        self.image_board.draw(1280 // 2 + 5, 960 // 2 - 2)

    # update():
    def update(self):
        pass

class TitleBackground:
    image_background = None
    image_title = None
    image_guide = None
    music = None

    def __init__(self):
        if not self.image_background:
            self.image_background = load_image('image\\background_title.jpg')
            self.image_title = load_image('image\\title.png')
            self.image_guide = load_image('image\\guide.png')
        if not self.music:
            self.music = load_music("sound\\background_title.mp3")
            self.music.set_volume(32)

        self.music.repeat_play()
    pass

    def draw(self):
        self.image_background.draw_to_origin(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.image_title.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 200, TITLE_WIDTH, TITLE_HEIGHT)
        if server.guide:
            self.image_guide.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 577, 819)


    def update(self):
        pass
