import pygame

# initialize pygame
pygame.init()
pygame.mixer.pre_init()

class ButtonImg:
    def __init__(self, pos, path, scale=1,
                 path_sound_hover=None,
                 path_sound_click=None):

        # load images
        img = pygame.image.load(path).convert_alpha()
        width, height = img.get_size()
        img = pygame.transform.smoothscale(img, (int(width * scale), int(height * scale)))

        # split images for frames
        width, height = img.get_size()
        height_single_frame = int(height / 3)
        self.img_list = []

        for i in range(3):
            img_crop = img.subsurface((0, i * height_single_frame,
                                       width, height_single_frame))
            self.img_list.append(img_crop)


        self.img = self.img_list[0]
        self.pos = pos
        self.state = None
        self.img_rect = self.img.get_rect()
        self.img_rect.topleft = self.pos
        self.path_hover_sound = path_sound_hover
        self.path_click_sound = path_sound_click
        if self.path_click_sound and self.path_hover_sound is not None:
            self.sound_hover = pygame.mixer.Sound(self.path_hover_sound)
            self.sound_click = pygame.mixer.Sound(self.path_click_sound)





    def draw(self, window):
        mouse_pos = pygame.mouse.get_pos()
        self.img = self.img_list[0]

        if self.img_rect.collidepoint(mouse_pos):

            # check if button clicked or hovered
            if pygame.mouse.get_pressed()[0]:
                self.img = self.img_list[2]
                if self.sound_click is not None and self.state != 'click':
                    self.sound_click.play()
                self.state = 'click'
            else:
                self.img = self.img_list[1]
                if self.sound_hover is not None and self.state != 'hover' and self.state != 'click':
                    self.sound_hover.play()
                self.state = 'hover'
        else:
            self.state = None

        window.blit(self.img, self.img_rect)

if __name__ == "__main__":

    # initialize display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My awesome game")

    # initialize clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # create objects
    button1 = ButtonImg((100, 100), "../Resources/Buttons/ButtonStart.png",
                        path_sound_hover="../../Resources/Sounds/hover.mp3",
                        path_sound_click="../../Resources/Sounds/click.mp3")


    # main loop
    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

        window.fill((255, 255, 255))
        button1.draw(window)

        pygame.display.update()

        clock.tick(fps)
