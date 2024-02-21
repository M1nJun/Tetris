import pygame

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

# game behavior
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

        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))
        self.sprites = pygame.sprite.Group()

        # was going to do tuple for the pos argument, but pygame had it's own vector implementation
        self.block = Block(self.sprites, pygame.Vector2(3,5), 'blue')

    def draw_grid(self):

        for col in range(1, COLS):
            x = col * CELL
            pygame.draw.line(self.surface, WHITE, (x,0), (x,self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL
            pygame.draw.line(self.surface, WHITE, (0,y), (self.surface.get_width(),y), 1)

    def run(self):
        
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        # blit is a fancy way of saying I want to put this surface on to another surface
        self.display_surface.blit(self.surface, (PADDING,PADDING))
        pygame.draw.rect(self.display_surface, WHITE, self.rect, 2, 2)

# discovered easy tool called sprite
class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        # group is required
        super().__init__(group)

        self.image = pygame.Surface((CELL, CELL))
        self.image.fill(color)

        # positioning
        # argument pos should be tuple that stands for the indices for the two dimensional grid
        x = pos.x * CELL
        y = pos.y * CELL
        self.rect = self.image.get_rect(topleft = (x,y))


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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.display_surface.fill(GRAY)

            self.game.run()
            self.score.run()
            self.preview.run()

            pygame.display.update()
            # for frame rate
            self.clock.tick()

if __name__ == '__main__':
    main = Main()
    main.run()