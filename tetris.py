import pygame
from random import choice
from os import path
import time

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

SCORE_DATA = {1: 50, 2: 100, 3: 500, 4: 1500}

DROP_SPEED = {1: 60, 2: 30, 3: 20, 4: 10}

class Game:
    def __init__(self, get_next_shape, update_score):

        # general
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))
        self.sprites = pygame.sprite.Group()

        self.get_next_shape = get_next_shape
        self.update_score = update_score

        # was going to do tuple for the pos argument, but pygame had it's own vector implementation
        # self.block = Block(self.sprites, pygame.Vector2(3,5), 'blue')

        # this is a nested list that is exactly the same size as the grid. For every cell 0 is initialized.
        self.occupancy = [[0 for x in range(COLS)] for y in range(ROWS)]
        # tetromino
        # self.sprites is the group argument
        self.tetromino = Tetromino(
            # 'I',
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.spawn_new_tetromino,
            self.occupancy)
        
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        # the higher the level, the higher the score you will get from the num lines you have cleared
        self.current_score += SCORE_DATA[num_lines] * self.current_level

        # every 10 lines += level by 1
        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
        self.update_score(self.current_lines, self.current_score, self.current_level)

    def display_end_screen(self):
        font = pygame.font.Font(path.join('.','PressStart.ttf'), 35)
        text_lines = [
            f"Lines cleared: {self.current_lines} ",
            f"Score: {self.current_score} ",
            f"Level: {self.current_level}"
        ]

        with open("highscore.txt", "a") as file:
            file.write("\n")
            file.writelines(text_lines)

        y = WINDOW_HEIGHT // 2 - len(text_lines) * 20 // 2
        for i, line in enumerate(text_lines):
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y + i * 40))
            self.display_surface.blit(text, text_rect)
            y += 30

        pygame.display.flip()

        self.music = pygame.mixer.Sound(path.join('.', 'audio', 'score.wav'))
        self.music.play()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.music = pygame.mixer.Sound(path.join('.', 'audio', 'proceed.wav'))
                    self.music.play()
                    time.sleep(1)
                    exit()

                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    self.music.stop()
                    self.music = pygame.mixer.Sound(path.join('.', 'audio', 'proceed.wav'))
                    self.music.play()
                    time.sleep(1)
                    exit()


    def check_game_over(self):
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                self.display_end_screen()

    # had to create a new argument for tetromino class to shift to allow new tetromino to spawn when curr tetromino hits the bottom
    def spawn_new_tetromino(self):
        # this is checking the previous tetromino. not the new one we're trying to create
        self.check_game_over()
        self.check_full_rows()
        self.tetromino = Tetromino(
            # 'I', # for testing purposes
            # this first arg used to be: choice(list(TETROMINOS.keys())),
            self.get_next_shape(),
            self.sprites,
            self.spawn_new_tetromino,
            self.occupancy)

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):

        for col in range(1, COLS):
            x = col * CELL
            pygame.draw.line(self.surface, WHITE, (x,0), (x,self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL
            pygame.draw.line(self.surface, WHITE, (0,y), (self.surface.get_width(),y), 1)

    def input_move(self):

        # checking the movement inputs of the user
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.tetromino.move_horizontal(-1)
        if keys[pygame.K_RIGHT]:
            self.tetromino.move_horizontal(1)
        if keys[pygame.K_DOWN]:
            self.tetromino.move_down()

    def input_rotate(self):
        # checking the rotation inputs of the user
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.tetromino.rotate()

    def run(self, block_fall_clock, block_move_clock, block_rotate_clock):
        
        
        if block_move_clock == 0: 
            self.input_move()
        if block_rotate_clock == 0:
            self.input_rotate()
        
        # update
        self.sprites.update()

        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        # blit is a fancy way of saying I want to put this surface on to another surface
        self.display_surface.blit(self.surface, (PADDING,PADDING))
        pygame.draw.rect(self.display_surface, WHITE, self.rect, 2, 2)

        if block_fall_clock == 0:
            self.tetromino.move_down()

    def check_full_rows(self):

        # get the full row indices
        delete_rows = []
        for i, row in enumerate(self.occupancy):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:
                # delete full rows
                for block in self.occupancy[delete_row]:
                    # kill is an inbuilt method of sprite. destorys sprite. removing it from group
                    block.kill()
                
                # move down blocks
                # for each row in occupancy
                for row in self.occupancy:
                    # for each block in that row
                    for block in row:
                        # if block actually exists
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

            
            # rebuild occupancy list
            self.occupancy = [[0 for x in range(COLS)] for y in range(ROWS)]
            for block in self.sprites:
                self.occupancy[int(block.pos.y)][int(block.pos.x)] = block

            # for updating score
            self.calculate_score(len(delete_rows))

class Tetromino:
    def __init__(self, shape, group, spawn_new_tetromino, occupancy):
        
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.spawn_new_tetromino = spawn_new_tetromino
        self.occupancy = occupancy

        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    # collisions
    def next_move_horizontal_collide(self, blocks, amount):
        # for every single block in blocks, call the horizontal_collide function with a new x position
        # the second argument is to hand over the occupancy list
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.occupancy) for block in self.blocks]
        # checking if there is at least one true value in collision_list
        return True if any(collision_list) else False
    
    def next_move_vertical_collide(self, blocks, amount):

        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.occupancy) for block in self.blocks]

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
        else:
            # before spawning a new tetromino, update the occupancy of the curr tetromino
            for block in self.blocks:
                # by default a vector has floating point numbers. But for indexing, you need an integer. So you need int conversion right before.
                # I really really wanted to use 1 for the occupancy value but gave up. Now it equals block.
                self.occupancy[int(block.pos.y)][int(block.pos.x)] = block
            self.spawn_new_tetromino()

    def rotate(self):
        # O shape doesn't rotate
        if self.shape != 'O':
            # need to think of a pivot
            # the first block of the blocks of a tetromino is always the pivot block
            pivot_pos = self.blocks[0].pos

            # new block positions
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            # to fix issue when you rotate a tetromino out of bounds
            for pos in new_block_positions:
                # horizontal check(left and right grid)
                if pos.x < 0 or pos.x >= COLS:
                    return

                # occupancy check(collision with other blocks)
                if self.occupancy[int(pos.y)][int(pos.x)]:
                    return

                # floor check
                if pos.y > ROWS:
                    return

            # 4 blocks
            for i,block in enumerate(self.blocks):
                # 4 blocks in new_bp too
                block.pos = new_block_positions[i]

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

    def rotate(self, pivot_pos):
        # disctance from curr block to the pivot point
        distance = self.pos - pivot_pos
        # rotation of the distance, not a new position
        rotated = distance.rotate(90)
        new_pos = pivot_pos + rotated
        return new_pos

    def horizontal_collide(self, x, occupancy):
        if not 0 <= x < COLS:
            return True

        if occupancy[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, occupancy):
        if y >= ROWS:
            return True
        
        # if there is a block in the position return true.
        # weird behavior than the horizontal one because the starting out y position is negative.
        if y >= 0 and occupancy[y][int(self.pos.x)]:
            return True

    def update(self):
        # self.pos -> rect
        x = self.pos.x * CELL
        y = self.pos.y * CELL
        self.rect = self.image.get_rect(topleft = (x,y))


class Preview:
    def __init__(self):
        # get window
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_R))
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDTH - PADDING, PADDING))

        # these are just letters
        # need dictionary of form {'L' : imported png of the tetromino}
        # a hardcoded path to the images isn't a great idea because different os can work differently
        # path join does the job of melting the path down to the right form
        # convert_alpha makes the image work better with pygame
        self.shape_surfaces = {shape: pygame.image.load(path.join('.', 'tetrominos', f'{shape}.png')).convert_alpha() for shape in TETROMINOS.keys()}
        # print(self.shape_surfaces)

        # want 1/3 of the preview height to place three items equaly on the screen
        self.partition_height = self.surface.get_height() / 3

    def run(self, next_shapes):

        self.surface.fill(GRAY)
        self.display_next_shapes(next_shapes)

        # displays the the surface on top of the display surface
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, WHITE, self.rect, 2, 2)

    def display_next_shapes(self, shapes):
        for i, shape in enumerate(shapes):
            #this surface is a local variable, different from the self.surface, which is an attribute of the preview class
            shape_surface = self.shape_surfaces[shape]
            x = self.surface.get_width() / 2
            y = self.partition_height / 2 + i * self.partition_height
            # met with a problem that the shapes appear starting from the x,y coords, so came up with a rect
            rect = shape_surface.get_rect(center = (x,y))
            self.surface.blit(shape_surface, rect)

class Score:
    def __init__(self):
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_R - PADDING))
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        self.display_surface = pygame.display.get_surface()

        # font
        self.font = pygame.font.Font(path.join('.','PressStart.ttf'), 15)

        self.partition_height = self.surface.get_height() / 3

        self.score = 0
        self.level = 1
        self.lines = 0

    def display_text(self, pos, text):
        text_surface = self.font.render(f'{text[0]}: {text[1]}', True, 'white')
        text_rect = text_surface.get_rect(center = pos)
        self.surface.blit(text_surface, text_rect)

    def run(self):

        self.surface.fill(GRAY)
        for i, text in enumerate([('Score', self.score), ('Level', self.level), ('Lines', self.lines)]):
            x = self.surface.get_width() / 2
            y = self.partition_height / 2 + i * self.partition_height
            self.display_text((x,y),text)

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, WHITE, self.rect, 2, 2)


# def main_menu(self):
#     run = True
#     while run:
#         font = pygame.font.Font(path.join('.','PressStart.ttf'), 50, bold=False, italic=True)
#         label = font.render('Press any key to begin', 1, (255, 255, 255))
#         self.surface.blit(label, (0 + WINDOW_WIDTH / 2 - (label.get_width()/2), 0 + WINDOW_HEIGHT/2 - (label.get_height()/2)))
#         pygame.display.update()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#             elif event.type == pygame.KEYDOWN:
#                 main(window)

class Main:
    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('TETRIS')

        # create mutiple shapes for preview
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()

        

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        # pop removes the first item from the list and returns it
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape
    
    def display_main_menu(self):
        font = pygame.font.Font(path.join('.','PressStart.ttf'), 27)
        text = font.render('Press any key to begin', 1, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        blink_timer = 0
        show_text = True

        self.display_surface.fill(GRAY)
        self.display_surface.blit(text, text_rect)
        pygame.display.flip()

        self.music = pygame.mixer.Sound(path.join('.', 'audio', 'main_menu.mp3'))
        self.music.play()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    self.music.stop()
                    self.music = pygame.mixer.Sound(path.join('.', 'audio', 'proceed.wav'))
                    self.music.play()
                    time.sleep(1)
            
            self.display_surface.fill(GRAY)
        
            if show_text:
                self.display_surface.blit(text, text_rect)

            if blink_timer >= FPS * 0.2:  # Blink every half second
                show_text = not show_text
                blink_timer = 0

            pygame.display.update()

            blink_timer += 1
            self.clock.tick(FPS)
    
    def run(self):
        self.display_main_menu()

        self.music = pygame.mixer.Sound(path.join('.', 'audio', 'background.mp3'))
        self.music.play()

        block_fall_clock = 0
        block_move_clock = 0
        block_rotate_clock = 0
        while True:
            
            # block_fall_clock = (block_fall_clock+1)%60
            block_fall_clock = (block_fall_clock+1)%DROP_SPEED[self.score.level]
            block_move_clock = (block_move_clock+1)%4
            block_rotate_clock = (block_rotate_clock+1)%7

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.music = pygame.mixer.Sound(path.join('.', 'audio', 'proceed.wav'))
                    self.music.play()
                    time.sleep(1)
                    pygame.quit()
                    exit()
            
            self.display_surface.fill(GRAY)

            self.game.run(block_fall_clock, block_move_clock, block_rotate_clock)
            self.score.run()
            self.preview.run(self.next_shapes)

            pygame.display.update()

            clock.tick(FPS)

if __name__ == '__main__':
    main = Main()
    main.run()