import pygame
from flappy_bird_game.misc import spritesheet
import scipy.misc
vec = pygame.math.Vector2
PLAYER_GRAV = 0.6
PLAYER_ACC = 0.5

class player():
    def __init__(self,game):
        self.game = game

        # spritesheet
        self.spritesheet = spritesheet.SpriteSheet(self.game.cwd + "/res/bird.png")
        self.bird_animations = []
        self._fill_bird_animations()
        self.curr_bird = pygame.transform.scale(self.bird_animations[0],(80,80))
        self.curr_index = 0

        # resize the bird images
        for f in range(len(self.bird_animations)):
            self.bird_animations[f] = pygame.transform.scale(self.bird_animations[f], (80, 80))

        # player postition variables
        self.pos = vec(100, 200)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def draw(self):
        # draws the player to the screen
        size_diff = self.curr_bird.get_rect().size[0] - 80
        xPos = self.game.player.pos.x - (size_diff / 2)
        yPos = self.game.player.pos.y - (size_diff / 2)
        self.game.screen.blit(self.curr_bird, (xPos, yPos))

    def flap(self):
        # allows the player to flap on the screen
        self.vel.y = 0
        self.vel.y -= 11.5

    def update(self):
        # equations of motion
        self.acc = vec(0, PLAYER_GRAV)
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # keeps the bird on the screen when it touches the ground
        if self.pos.y >= 450:
            self.pos.y = 450

        # flapping animation
        if self.game.timer % 6 == 0:
            self.curr_bird = self.bird_animations[self.curr_index]
            self.curr_index += 1
            if self.curr_index > 3:
                self.curr_index = 0

        # rotation animation
        if self.game.timer % 6 == 0:
            self.rotation()

    def rotation(self):
        # controls how the bird rotates while it is in the air depending on the velocity
        curr_y_vec = self.game.player.vel.y
        angle = (-(6 * min(curr_y_vec,15)) if curr_y_vec >= 0 else 30)
        self.curr_bird = pygame.transform.rotate(self.curr_bird, angle)

    def _fill_bird_animations(self):
        # fills the list with the possible bird flapping positions
        sprite_size = self.spritesheet.sprite_sheet.get_rect().size
        length = 28
        for f in range(3):
            self.bird_animations.append(self.spritesheet.get_image(f * length, sprite_size[1] - length, length, length))
        self.bird_animations.append(self.spritesheet.get_image(length, sprite_size[1] - length, length, length))

    def getScreen(self,width=None,height=None):
        # get a numpy array of the screen
        screen_array = pygame.surfarray.array3d(self.game.screen)
        if width:
            resized_image = scipy.misc.imresize(screen_array, (width, height, 3))
        return resized_image

    def save_image(self,array):
        # saves the screen
        shape = array.shape
        surface = pygame.Surface((shape[0], shape[1]))
        pygame.surfarray.blit_array(surface, array)
        pygame.image.save(surface, 'state.png')

