import pygame
import Scene_manager


def Menu():
    pygame.init()
    pygame.event.clear()

    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Menu")

    fps = 30
    clock = pygame.time.Clock()


    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    Scene_manager.open_scene("Game")
                    print('S')

        window.fill((255, 255, 255))
        display_text = "Menu - press s to go to Game"
        font = pygame.font.Font("../Resources/Marcellus-Regular.ttf", 50)
        text = font.render(display_text, True, (0, 0, 200))
        window.blit(text, (350, 300))

        pygame.display.update()

        clock.tick(fps)

if __name__ == "__main__":
    Menu()