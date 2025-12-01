import pygame
import Scene_Manager


def game():
    pygame.init()
    pygame.event.clear()

    width, height = 1280, 720

    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Fruit Ninja")

    fps = 30
    clock = pygame.time.Clock()


    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    Scene_Manager.open_scene("Menu")

        window.fill((255, 255, 255))
        font = pygame.font.Font("../../Resources/Marcellus-Regular.ttf", 50)
        text = "Press A to go to Menu"
        text_menu = font.render(text, True, (0, 0, 200))
        window.blit(text_menu, (400, 300))


        pygame.display.update()

        clock.tick(fps)

if __name__ == "__main__":
    game()