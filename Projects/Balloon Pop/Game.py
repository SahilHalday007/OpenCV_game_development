import pygame
import Scene_manager
import cv2
import numpy as np
import random
import os
import time
from cvzone.HandTrackingModule import HandDetector

class Balloon:
    def __init__(self, pos, path, scale=1, grid=(2, 4),
                 animation_frames=None, animation_speed=1, speed=10, path_sound_pop=None):
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
        self.path_sound_pop = path_sound_pop
        if self.path_sound_pop:
            self.sound_pop = pygame.mixer.Sound(self.path_sound_pop)


    def draw(self, window):
        if self.is_animating is False:
            self.rect_img.y -= self.speed
        window.blit(self.img, self.rect_img)

    def check_pop(self, x, y):
        # check for the hit
        if self.rect_img.collidepoint(x, y) and self.is_animating is False:
            self.is_animating = True
            if self.path_sound_pop:
                self.sound_pop.play()


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

    # variables
    balloons = []
    start_time = time.time()
    time_interval = 1
    speed = 5

    # create hand detector
    detector = HandDetector(maxHands=1, detectionCon=0.8)

    # get all balloon paths
    path_balloon_folder = "../../Resources/Project - Balloon Pop/Balloons/"
    path_list_balloons = os.listdir(path_balloon_folder)

    # balloon generator
    def generate_balloon():
        random_balloon_path = path_list_balloons[random.randint(0, len(path_list_balloons) - 1)]
        x = random.randint(100, img.shape[1] - 100)
        y = img.shape[0]
        random_scale = round(random.uniform(0.3, 0.7), 2)

        balloons.append(Balloon((x, y), path=os.path.join(path_balloon_folder, random_balloon_path),
                        grid=(3, 4), scale=random_scale, speed=speed, path_sound_pop="../../Resources/Project - Balloon Pop/Pop.wav"))

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
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, draw=False, flipType=False)


        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))

        if hands:
            hand = hands[0]
            x, y = hand['lmList'][8][:2]
            pygame.draw.circle(window, (0, 0, 200), (x, y), 20)
            pygame.draw.circle(window, (200, 200, 200), (x, y), 16)

        else:
            x, y = 0, 0


        for balloon in balloons:
            balloon.draw(window)
            balloon.check_pop(x, y)

        if time.time() - start_time > time_interval:
            time_interval = random.uniform(0.3, 0.8)
            generate_balloon()
            speed += 1
            start_time = time.time()

        # update display
        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    Game()