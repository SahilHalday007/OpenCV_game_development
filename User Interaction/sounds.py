import pygame

# initialize pygame
pygame.init()

# initialize display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My awesome game")

# initialize clock for FPS
fps = 30
clock = pygame.time.Clock()

# load sounds
pygame.mixer.pre_init()
pygame.mixer.music.load("../Resources/Sounds/timer.mp3")
pygame.mixer.music.play()

sound_click = pygame.mixer.Sound("../Resources/Sounds/click.mp3")

# variables
counter = 0

# main loop
start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    window.fill((255, 255, 255))
    counter +=1
    if counter > 60:
        sound_click.play()
        counter = 0

    # update display
    pygame.display.update()

    clock.tick(fps)
