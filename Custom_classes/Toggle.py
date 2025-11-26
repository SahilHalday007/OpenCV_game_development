import pygame

# initialize pygame
pygame.init()
pygame.mixer.pre_init()


class ToggleImg:
    def __init__(self, pos, img_path, scale=1, path_click_sound=None):

        # load images
        img = pygame.image.load(img_path).convert_alpha()
        width, height = img.get_size()
        img = pygame.transform.smoothscale(img, (int(width * scale), int(height * scale)))

        # split images for frames
        width, height = img.get_size()
        height_single_frame = int(height / 2)
        img_list = []

        for i in range(2):
            img_crop = img.subsurface((0, i * height_single_frame,
                                       width, height_single_frame))
            img_list.append(img_crop)

        self.img_off = img_list[0]
        self.img_on = img_list[1]
        self.state = None
        self.img = self.img_off
        self.img_rect = self.img_off.get_rect()
        self.img_rect.topleft = pos
        self.path_click_sound = path_click_sound
        if self.path_click_sound is not None:
            self.sound_click = pygame.mixer.Sound(self.path_click_sound)

        self.counter = -1

    def draw(self, window):
        # # check mouse position
        mouse_pos = pygame.mouse.get_pos()


        if self.img_rect.collidepoint(mouse_pos):

            # check if button is clicked
            if pygame.mouse.get_pressed()[0] and self.counter == -1:
                self.counter = 0
                if self.sound_click is not None:
                    self.sound_click.play()
                if self.state == 'on':
                    self.state = 'off'
                else:
                    self.state = 'on'

        if self.counter != -1:
            self.counter += 1
            if self.counter > 5:
                self.counter = -1

        if self.state == 'on':
            self.img = self.img_on
        else:
            self.img = self.img_off

        window.blit(self.img, self.img_rect)

if __name__ == "__main__":

    # initialize display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My awesome game")

    # initialize clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # toggle
    toggle_list = []
    for x in range(8):
        for y in range(9):
            toggle_list.append(ToggleImg(((x * (100+50))+50, (y * 70) +50), "../Resources/Toggle/ToggleGreen.png",
                                path_click_sound="../Resources/Sounds/click.mp3"))

    # main loop
    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

        window.fill((255, 255, 255))
        for toggle in toggle_list:
            toggle.draw(window)

        # update display
        pygame.display.update()
        clock.tick(fps)
