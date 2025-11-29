import pygame
import Scene_manager
from Custom_classes.Button import ButtonImg


def menu():
    # initialize pygame
    pygame.init()
    pygame.event.clear()

    # initialize display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Menu")

    # initialize clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # load images
    img_bg = pygame.image.load("../../Resources/Project - Balloon Pop/BackgroundBalloonPop.png").convert()

    # buttons
    button_start = ButtonImg((465, 420), "../../Resources/Buttons/ButtonStart.png",
                             path_click_sound="../../Resources/Sounds/click.mp3",
                             path_hover_sound="../../Resources/Sounds/hover.mp3")

    # load music
    pygame.mixer.pre_init()
    pygame.mixer.music.load("../../Resources/Project - Balloon Pop/BackgroundMusicMenu.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

    # main loop
    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    Scene_manager.open_scene("Game")

        # draw the background image
        window.blit(img_bg, (0, 0))
        button_start.draw(window)

        # check if button was clicked
        if button_start.state == 'click':
            pygame.mixer.music.stop()
            Scene_manager.open_scene("Game")

        # update display
        pygame.display.update()
        clock.tick(fps)

if __name__ == "__main__":
    menu()