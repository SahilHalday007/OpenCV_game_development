import pygame

# initialize pygame
pygame.init()

# initialize display / window
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My awesome game")

# initialize clock for FPS
fps = 30
clock = pygame.time.Clock()


start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            key = event.key
            match key:
                case pygame.K_a:
                    print("A")
                case pygame.K_s:
                    print("S")
                case pygame.K_UP:
                    print("UP")
                case pygame.K_DOWN:
                    print("DOWN")


    window.fill((255, 255, 255))

    pygame.display.update()

    clock.tick(fps)
