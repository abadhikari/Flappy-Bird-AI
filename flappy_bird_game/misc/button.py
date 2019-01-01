import pygame

class button:
    def __init__(self, img, x, y, width, height, text=''):
        self.img = img
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = pygame.transform.scale(self.img,(self.width,self.height))

    def draw(self, win):
        # Call this method to draw the button on the screen
        win.blit(self.img, (self.x, self.y))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < (self.x + self.width):
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        else:
            return False
