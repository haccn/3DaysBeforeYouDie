class HitFlash:
    def __init__(self, duration = 0.1):
        self.duration = 0.1
        self.timer = 0.

        self.no_color = (0, 0, 0)
        self.hl_color = (255, 255, 255)
        self.color_to_add = self.no_color

    def begin(self):
        self.timer = self.duration

    def update(self, deltatime):
        if self.timer > 0:
            self.timer -= deltatime
            self.color_to_add = self.hl_color
        else:
            self.color_to_add = self.no_color

