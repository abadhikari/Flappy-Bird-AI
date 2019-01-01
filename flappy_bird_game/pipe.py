import random
import pygame
from flappy_bird_game.misc.deque import DoublyLinkedList

class pipe():
    def __init__(self, game):
        self.game = game
        self.pipe = pygame.transform.scale(self.game.player.spritesheet.get_image(84, 320, 28, 160), (80,450))
        self.flipped_pipe = pygame.transform.flip(self.pipe, False, True)

        # pipe variables
        self.b_pipes = DoublyLinkedList()
        self.t_pipes = DoublyLinkedList()
        self.b_pipes_pos = DoublyLinkedList()
        self.t_pipes_pos = DoublyLinkedList()

        # fill pipes
        for i in range(3):
            self.make_pipe()

    def update(self):
        # updates position of the pipes, score, and reward of the agent
        pass_through = 0
        b_head, t_head, b_pos_head, t_pos_head = self.b_pipes._head, self.t_pipes._head, self.b_pipes_pos._head, self.t_pipes_pos._head
        for i in range(len(self.b_pipes)):
            if b_pos_head.data[0] < -80:
                self.make_pipe()
                self.remove_first_pipes()

            if b_pos_head.data[0] - 15 in [self.game.player.pos.x - y for y in range(7)]:
                self.game.score += 1
                pass_through = 1

            b_pos_head.data[0] -= 3.5
            t_pos_head.data[0] -= 3.5

            b_head, t_head, b_pos_head, t_pos_head = b_head.link, t_head.link, b_pos_head.link, t_pos_head.link

        return pass_through

    def draw(self):
        # draws the pipes to the screen
        b_head, t_head, b_pos_head, t_pos_head = self.b_pipes._head, self.t_pipes._head, self.b_pipes_pos._head, self.t_pipes_pos._head
        for i in range(len(self.b_pipes)):
            self.game.screen.blit(b_head.data, b_pos_head.data)
            self.game.screen.blit(t_head.data, t_pos_head.data)
            b_head, t_head, b_pos_head, t_pos_head = b_head.link, t_head.link, b_pos_head.link,t_pos_head.link

    def remove_first_pipes(self):
        # removes the first set of pipes
        self.b_pipes.removefirst()
        self.t_pipes.removefirst()
        self.b_pipes_pos.removefirst()
        self.t_pipes_pos.removefirst()

    def reset_pipes(self):
        self.__init__(self.game)

    def checkCollision(self):
        # only used rectangles for collision detection so had to hard code several values
        player_rect = pygame.Rect(self.game.player.pos.x+22, self.game.player.pos.y+25,27,25)
        t_pipe_rect = pygame.Rect(self.t_pipes.peek_first().get_rect())
        t_pipe_rect.left, t_pipe_rect.top = self.t_pipes_pos.peek_first()[0], self.t_pipes_pos.peek_first()[1] - 8
        b_pipe_rect = pygame.Rect(self.b_pipes.peek_first().get_rect())
        b_pipe_rect.left, b_pipe_rect.top = self.b_pipes_pos.peek_first()[0], self.b_pipes_pos.peek_first()[1] + 8

        if player_rect.colliderect(t_pipe_rect) or player_rect.colliderect(b_pipe_rect):
            return True

        # if bird hits the ground or goes too far above the screen
        if self.game.player.pos.y >= 450 or self.game.player.pos.y < -100:
            return True

        return False

    def make_pipe(self):
        # makes pipes using random numbers between stated boundries
        space_between_pipes = 140
        pipe_size = self.pipe.get_rect().size
        top_pos = [250]

        if len(self.b_pipes) != 0:
            top_pos = self.t_pipes_pos.peek_last()

        random_number = random.randrange(100, 260)
        top_pipe_pos = [top_pos[0] + 250, random_number - pipe_size[1]]
        bottom_pipe_pos = [top_pos[0] + 250, random_number + space_between_pipes]

        self.b_pipes.addlast(self.pipe)
        self.t_pipes.addlast(self.flipped_pipe)
        self.b_pipes_pos.addlast(bottom_pipe_pos)
        self.t_pipes_pos.addlast(top_pipe_pos)



