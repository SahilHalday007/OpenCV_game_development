import pygame

pygame.init()

width, height = 1280, 720

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Myy awesome game")

fps = 30
clock = pygame.time.Clock()

start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    window.fill((255, 0, 0))

    pygame.display.update()

    clock.tick(fps)