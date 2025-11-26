import pygame

pygame.init()

width, height = 1280, 720

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My awesome game")

fps = 30
clock = pygame.time.Clock()

# load images
imgRedBalloon = pygame.image.load("../Resources/BalloonRed.png").convert_alpha()
imgBackground = pygame.image.load("../Resources/BackgroundBlue.jpg").convert()

rectBalloon = imgRedBalloon.get_rect()

start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
            
    rectBalloon.x += 5

    window.blit(imgBackground, (0, 0))
    pygame.draw.rect(window, (0, 255, 0), rectBalloon)
    window.blit(imgRedBalloon, rectBalloon)

    pygame.display.update()

    clock.tick(fps)
