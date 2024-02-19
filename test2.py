import pygame
pygame.init()

screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Test2 Game")

RED = [255, 0, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
YELLOW = [255, 255, 0]
GREEN = [0, 255, 0]

birthday_image = pygame.image.load('birthday.jpeg')
birthday_image = pygame.transform.scale(birthday_image, (screen_width, screen_height))

#Generic code for loading an image into pygame and picking a center
cat_img = pygame.image.load('cat.png')
cat_img = pygame.transform.scale(cat_img, (300, 200))
cat_rect = cat_img.get_rect()
cat_rect.center = [400, 400]

shiba_img = pygame.image.load('shiba.png')
shiba_img = pygame.transform.scale(shiba_img, (300, 300))
shiba_rect = shiba_img.get_rect()
shiba_rect.center = [800, 400]

cat_x = 200
cat_y = 0

shiba_x = 500
shiba_y = screen_width - 300

direction = 'right'


running = True
while running:
    screen.blit(birthday_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(cat_img, cat_rect)
    screen.blit(shiba_img, shiba_rect)

    if direction == 'right':
        cat_x = cat_x + 5
        if cat_x > screen_width - 300:
            direction = 'left'
            cat_img = pygame.transform.flip(cat_img, True, False)
    elif direction == 'left':
        cat_x = cat_x - 5
        if cat_x < 0:
            direction = 'right'
            cat_img = pygame.transform.flip(cat_img, True, False)
    screen.blit(cat_img, [cat_x, cat_y])
    pygame.display.flip()

pygame.quit()