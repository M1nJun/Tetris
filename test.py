import pygame

s_width = 800  # window width
s_height = 800  # window height

pygame.init()

screen = pygame.display.set_mode([s_width, s_height])

screen.fill((0, 0, 0))
pygame.display.flip()

# Wait for the user to close the window
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
