import pygame
import Scene_manager
from Custom_classes.Button import ButtonImg


def Game():
    pygame.init()
    pygame.event.clear()

    # initialize display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game")

    # initialize clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # load images
    img_bg = pygame.image.load("../../Resources/Project - Balloon Pop/BackgroundBalloonPop.png").convert_alpha()

    # main loop
    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    Scene_manager.open_scene("Menu")

        # apply logic
        window.blit(img_bg, (0, 0))

        # update display
        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    Game()