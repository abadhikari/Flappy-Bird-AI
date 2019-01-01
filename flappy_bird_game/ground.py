class ground():
    def __init__(self,game):
        self.game = game
        self.ground = self.game.load_image(self.game.cwd + "/res/ground.png")
        self.ground_x = 0

    def draw(self):
        # simply draws the ground to the screen
        for f in range(3):
            self.game.screen.blit(self.ground, (self.ground_x + (480 * f), 500))
        if not self.game.game_over:
            self.ground_x -= 3.5
            if self.ground_x < -500:
                self.ground_x = 0

