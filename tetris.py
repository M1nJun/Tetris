import pygame
from random import choice

FPS = 200
clock = pygame.time.Clock()

PADDING = 20

# game
COLS = 10  # 10 columns
ROWS = 20  # 20 rows
CELL = 40
GAME_WIDTH, GAME_HEIGHT = COLS * CELL, ROWS * CELL

# side bar
SIDEBAR_WIDTH = 200
PREVIEW_HEIGHT_R = 0.7
SCORE_HEIGHT_R = 1 - PREVIEW_HEIGHT_R

# window
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

# game behaviour 
UPDATE_START_SPEED = 200
MOVE_WAIT_TIME = 200
ROTATE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLS // 2, -1)

# Colors 
YELLOW = '#f1e60d'
RED = '#e51b20'
BLUE = '#204b9b'
GREEN = '#65b32e'
PURPLE = '#7b217f'
CYAN = '#6cc6d9'
ORANGE = '#f07e13'
GRAY = '#1C1C1C'
WHITE = '#FFFFFF'

# shapes
# keys are the original shapes of the tetrominos
# Inside of the grid, imagine the center of your shape to be (0,0)
# the rest of the configurations are in respect to that center
# for example: the T shape would look like:
#         (0,1)
# (-1,0)  (0,0)  (1,0)
# this is specifically done to make the implementation of the tetrominos class easier

TETROMINOS = {
	'T': {'shape': [(0,0), (-1,0), (1,0), (0,-1)], 'color': PURPLE},
	'O': {'shape': [(0,0), (0,-1), (1,0), (1,-1)], 'color': YELLOW},
	'J': {'shape': [(0,0), (0,-1), (0,1), (-1,1)], 'color': BLUE},
	'L': {'shape': [(0,0), (0,-1), (0,1), (1,1)], 'color': ORANGE},
	'I': {'shape': [(0,0), (0,-1), (0,-2), (0,1)], 'color': CYAN},
	'S': {'shape': [(0,0), (-1,0), (0,-1), (1,-1)], 'color': GREEN},
	'Z': {'shape': [(0,0), (1,0), (0,-1), (-1,-1)], 'color': RED}
}

SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}

class Game:
    def __init__(self):

        # general
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))
        self.sprites = pygame.sprite.Group()

        # was going to do tuple for the pos argument, but pygame had it's own vector implementation
        self.block = Block(self.sprites, pygame.Vector2(3,5), 'blue')

        # tetromino
        # self.sprites is the group argument
        self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), self.sprites)



    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):

        for col in range(1, COLS):
            x = col * CELL
            pygame.draw.line(self.surface, WHITE, (x,0), (x,self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL
            pygame.draw.line(self.surface, WHITE, (0,y), (self.surface.get_width(),y), 1)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.tetromino.move_horizontal(-1)
        if keys[pygame.K_RIGHT]:
            self.tetromino.move_horizontal(1)

    def run(self, i, j):
        
        # update
        if j == 0:
            self.input()
        self.sprites.update()

        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        # blit is a fancy way of saying I want to put this surface on to another surface
        self.display_surface.blit(self.surface, (PADDING,PADDING))
        pygame.draw.rect(self.display_surface, WHITE, self.rect, 2, 2)

        if i == 0:
            self.tetromino.move_down()


class Tetromino:
    def __init__(self, shape, group):
        
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']

        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    # collisions
    def next_move_horizontal_collide(self, blocks, amount):
        # for every single block in blocks, call the horizontal_collide function with a new x position
        collision_list = [block.horizontal_collide(int(block.pos.x + amount)) for block in self.blocks]
        # checking if there is at least one true value in collision_list
        return True if any(collision_list) else False
    
    def next_move_vertical_collide(self, blocks, amount):

        collision_list = [block.vertical_collide(int(block.pos.y + amount)) for block in self.blocks]

        return True if any(collision_list) else False

    # movement
    def move_horizontal(self, amount):
        # We will allow only horizontal movement when you are in bounds
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):

        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1


# discovered easy tool called sprite
class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        # group is required
        super().__init__(group)

        self.image = pygame.Surface((CELL, CELL))
        self.image.fill(color)

        # positioning
        # argument pos should be tuple that stands for the indices for the two dimensional grid

        # the shape positions in the tetrominos dictionaries are in tuples
        # but the block class is expecting a pygame Vector, need to convert
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        x = self.pos.x * CELL
        y = self.pos.y * CELL
        # another issue faced was that since the positions had negative values,
        # if the tetromino was created at the very topleft, it went outside the screen
        self.rect = self.image.get_rect(topleft = (x,y))

    def horizontal_collide(self, x):
        if not 0 <= x < COLS:
            return True

    def vertical_collide(self, y):
        if y >= ROWS:
            return True

    def update(self):
        # self.pos -> rect
        x = self.pos.x * CELL
        y = self.pos.y * CELL
        self.rect = self.image.get_rect(topleft = (x,y))


# pygame doesn't have a built-in timer
# 1 sec = 1 milisec
# for time, you need to think about in-terms of the starting point



    

class Preview:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_R))
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDTH - PADDING, PADDING))

    def run(self):
        self.display_surface.blit(self.surface, self.rect)

class Score:
    def __init__(self):
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_R - PADDING))
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        self.display_surface = pygame.display.get_surface()

    def run(self):
        self.display_surface.blit(self.surface, self.rect)

class Main:
    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('TETRIS')

        self.game = Game()
        self.score = Score()
        self.preview = Preview()
    
    def run(self):
        i = 0
        j = 0
        while True:
            i = (i+1)%60
            j = (j+1)%4

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.display_surface.fill(GRAY)

            self.game.run(i, j)
            self.score.run()
            self.preview.run()

            pygame.display.update()

            clock.tick(FPS)


if __name__ == '__main__':
    main = Main()
    main.run()