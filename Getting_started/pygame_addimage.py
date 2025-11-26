import pygame

pygame.init()

width, height = 1280, 720

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My awesome game")

fps = 30
clock = pygame.time.Clock()

# load images
imgBackground = pygame.image.load("../Resources/BackgroundBlue.jpg").convert()
imgBalloonRed = pygame.image.load("../Resources/BalloonRed.png").convert_alpha()

start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    window.fill((255, 255, 255))
    window.blit(imgBackground, (0, 0))
    window.blit(imgBalloonRed, (600, 200))

    pygame.display.update()

    clock.tick(fps)
