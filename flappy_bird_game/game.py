import pygame
import time
import flappy_bird_game.ground as ground
import flappy_bird_game.pipe as pipe
import flappy_bird_game.player as player
import os

HEADLESS = False
GET_IMAGE = False

if HEADLESS:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

class gameEnv():

    def __init__(self, width=500, height=580):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")

        # to access the res folder
        self.cwd = os.getcwd().replace('\\','/')
        if self.cwd[-1] == 'k':
            self.cwd = self.cwd[:-20] + "/flappy_bird_game"

        # screen
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

        self.resized_dimensions = (84,84)
        if HEADLESS:
            self.screen = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, width, height), 0)

        # game variables
        self.game_over = False
        self.high_score = 0
        self.score = 0
        self.pass_through = 0
        self.frame_skip = 4

        # game elements
        self.background = self.load_image(self.cwd + "/res/background.png")
        self.player = player.player(self)
        self.pipe = pipe.pipe(self)
        self.ground = ground.ground(self)

        # frame variables
        self.initial_time = time.time()
        self.curr_time = 0
        self.total_time = 0
        self.timer = 0
        self.fps = 60
        self.time_per_tick = 1/self.fps
        self.last_tick_time = 0

    def update(self):
        self.player.update()
        if not self.game_over:
            # updates the agent reward
            self.pass_through = self.pipe.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.pipe.draw()
        self.ground.draw()
        self.player.draw()

        # render the score and high score
        my_font = pygame.font.SysFont("monospace", 16)
        high_score_text = my_font.render("HighScore: {0}".format(self.high_score), 1, (0, 0, 0))
        score_text = my_font.render("Score: {0}".format(self.score), 1, (0, 0, 0))

        # score on the top lefthand side if the game isn't over
        score_x,score_y = (5,10)
        self.screen.blit(high_score_text, (score_x, score_y))
        self.screen.blit(score_text, (score_x + 13, score_y + 20))

        pygame.display.flip()

    def load_image(self, string):
        return pygame.image.load(string).convert_alpha()

    def reset(self):
        # re-initailize game variables
        self.game_over = False
        self.player = player.player(self)
        self.score = 0
        self.pipe.reset_pipes()
        # run the game
        self.run()

        # return the initial state
        return self.player.getScreen(self.resized_dimensions[0],self.resized_dimensions[1])

    def step(self,action):
        # steps the env and returns the new state, reward, and the done
        self.run()
        image = self.player.getScreen(self.resized_dimensions[0],self.resized_dimensions[1])
        # to save an image
        if GET_IMAGE and self.timer > 40:
            self.player.save_image(image)
        if self.timer % self.frame_skip == 0 and action == 1:
            self.player.flap()
        return image, self.pass_through, self.game_over

    def run(self):
        # keeps track of the time for the fps
        self.curr_time = time.time()
        self.total_time += (self.curr_time - self.initial_time)
        self.last_tick_time += (self.curr_time - self.initial_time)
        self.initial_time = self.curr_time

        # keeps everything running at the intended fps
        if self.last_tick_time > self.time_per_tick:
            self.update()

            # check score
            if self.score > self.high_score:
                self.high_score = self.score

            # check for collisions
            if self.pipe.checkCollision():
                self.game_over = True

            self.draw()
            self.timer += 1
            self.last_tick_time = 0

        if self.total_time > 1:
            print(self.timer)
            self.total_time = 0
            self.timer = 0

'''env = gameEnv()
num_ep = 10
init_time = time.time()
curr_time = 0
total_time = 0

for f in range(num_ep):
    s = env.reset()
    d = False
    j = 0

    while True:
        j += 1
        action = 0

        curr_time = time.time()
        total_time += (curr_time - init_time)
        init_time = curr_time

        if j > 50:
            print(total_time)
            total_time = 0
            action = 1
            j = 0
        s1,r,d = env.step(action)

        if d:
            break'''

