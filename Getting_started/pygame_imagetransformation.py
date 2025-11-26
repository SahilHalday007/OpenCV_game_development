import pygame

pygame.init()

width, height = 1028, 720

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Awesome Game")

# load images
imgBalloonRed = pygame.image.load("../Resources/BalloonRed.png").convert_alpha()
imgBackgroundBlue = pygame.image.load("../Resources/BackgroundBlue.jpg").convert()

# transform images
imgBalloonRed = pygame.transform.rotozoom(imgBalloonRed, 45, 1 )

fps = 30
clock = pygame.time.Clock()

start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    window.blit(imgBackgroundBlue, (0, 0))
    window.blit(imgBalloonRed, (400, 200))


    pygame.display.update()

    clock.tick(fps)