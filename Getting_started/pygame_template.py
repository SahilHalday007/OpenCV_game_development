import pygame

pygame.init()

width, height = 1280, 720

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My awesome game")

fps = 30
clock = pygame.time.Clock()


start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    window.fill((255, 255, 255))

    red, green, blue = ((255, 0, 0), (0, 255, 0), (0, 0, 255))

    pygame.draw.polygon(window, red, ((491, 100), (788, 100), (937, 357),
                                            (788, 614), (491, 614), (342, 357)))

    pygame.draw.circle(window, green, (640, 360), 200)

    pygame.display.update()

    clock.tick(fps)
