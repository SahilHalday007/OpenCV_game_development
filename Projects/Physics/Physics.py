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
body_segment = pymunk.Body(body_type=pymunk.Body.STATIC)

# create shape
shape = pymunk.Circle(body, 15)
shape.density = 1
shape.elasticity = 0.5
shape_segment = pymunk.Segment(body_segment, (0, 150), (800, 50), 2)
shape_segment.elasticity = 1

# add to space
space.add(body, shape)
space.add(body_segment, shape_segment)

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
    pygame.draw.line(window, (0, 0, 0), (8, 650), (800, 750), 5)

    # update display
    pygame.display.update()
    clock.tick(fps)
    space.step(1 / fps)
