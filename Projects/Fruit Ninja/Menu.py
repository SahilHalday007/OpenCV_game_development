import pygame
import Scene_Manager
from Custom_classes.Button import ButtonImg


def menu():
    # initiate pygame
    pygame.init()
    pygame.event.clear()

    # initialize window
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Menu")

    # initialize clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # load images
    img_bg = pygame.image.load("../../Resources/Project - Fruit Ninja/BackgroundMenu.png")

    # buttons
    start_button = ButtonImg((500, 290), "../../Resources/Project - Fruit Ninja/ButtonStart.png",
                             path_hover_sound="../../Resources/Sounds/hover.mp3",
                             path_click_sound="../../Resources/Sounds/click.mp3")

    # main loop
    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()


        window.blit(img_bg, (0, 0))
        start_button.draw(window)

        if start_button.state == "click":
            Scene_Manager.open_scene("Game")


        # update window
        pygame.display.update()
        clock.tick(fps)

if __name__ == "__main__":
    menu()