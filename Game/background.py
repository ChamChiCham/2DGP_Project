from pico2d import load_image

class Background:
    image = None

    def __init__(self):
        if self.image == None:
            self.image = load_image('image_background_playing.jpg')

    def draw(self):
        self.image.draw(1280 // 2, 960 // 2)

    def update(self):
        pass