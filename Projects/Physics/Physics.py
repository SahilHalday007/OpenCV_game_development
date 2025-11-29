import pymunk
import pygame

# initialize pygame
pygame.init()

width, height = 800, 800

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physics")

# initialize clock for FPS
fps = 30
clock = pygame.time.Clock()

# initialize pymunk space
space = pymunk.Space()
space.gravity = 0.0, -100.0

# create body
body = pymunk.Body()
body.position = 500, 800

# create shape
shape = pymunk.Circle(body, 15)
shape.density = 1

# add to space
space.add(body, shape)

# main loop
start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    window.fill((255, 255, 255))

    # display
    x, y = body.position[0], height - body.position[1]
    pygame.draw.circle(window, (0, 0, 255), (int(x), int(y)), 15)

    # update display
    pygame.display.update()
    clock.tick(fps)
    pymunk.step(1 / fps)
