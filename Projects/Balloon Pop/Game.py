import pygame
import Scene_manager
import cv2
import numpy as np

class Balloon:
    def __init__(self, pos, path, scale=1, grid=(2, 4),
                 animation_frames=None, animation_speed=1, speed=10):
        # load images
        img = pygame.image.load(path).convert_alpha()
        width, height = img.get_size()
        img = pygame.transform.smoothscale(img, (int(width * scale), int(height * scale)))
        width, height = img.get_size()

        #  split images for frames
        if animation_frames is None:
            animation_frames = grid[0] * grid[1]
        width_single_frame = width / grid[1]
        height_single_frame = height / grid[0]
        self.img_list = []
        counter = 0

        for row in range(grid[0]):
            for col in range(grid[1]):
                counter += 1
                if counter <= animation_frames:
                    img_crop = img.subsurface((col * width_single_frame, row * height_single_frame,
                                               width_single_frame, height_single_frame))

                    self.img_list.append(img_crop)

        self.img = self.img_list[0]
        self.rect_img = self.img.get_rect()
        self.rect_img.x, self.rect_img.y = pos[0], pos[1]
        self.pos = pos
        self.path = path
        self.animation_count = 0
        self.animation_speed = animation_speed
        self.is_animating = False
        self.speed = speed


    def draw(self, window):
        if self.is_animating is False:
            self.rect_img.y -= self.speed
        window.blit(self.img, self.rect_img)

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

    # initialize opencv webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # balloons
    ballon1 = Balloon((100, 300), "../../Resources/Project - Balloon Pop/Balloons/BalloonRed.png",
                      grid=(3, 4))

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
        # openCV
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))

        ballon1.draw(window)


        # update display
        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    Game()