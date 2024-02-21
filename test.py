import pygame

s_width = 800  # window width
s_height = 800  # window height

pygame.font.init()
filepath = './highscore.txt'
fontpath = './arcade.ttf'
fontpath_mario = './mario.ttf'
col = 10  # 10 columns
row = 20  # 20 rows
play_width = 300  # play window width; 300/10 = 30 width per block
play_height = 600  # play window height; 600/20 = 20 height per block
block_size = 30  # size of block

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

pygame.init()

screen = pygame.display.set_mode([s_width, s_height])

def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(fontpath, size)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, top_left_y + play_height/2 - label.get_height()/2))

running = True
while running:
    screen.fill((0, 0, 0))  # Fill the screen with black
    draw_text_middle('Press any key to begin', 50, (255, 255, 255), screen)
    pygame.display.update()  # Update the display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # Check if any key is pressed
            running = False  # Quit the loop if any key is pressed

pygame.quit()
