import pygame
import Scene_manager
import cv2
import numpy as np
import random
import os
import time
import math
import threading
from cvzone.HandTrackingModule import HandDetector
from Custom_classes.Button import ButtonImg


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
        self.pop = False
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

        if self.is_animating:
            # Loop through all the frames
            if self.animation_count != len(self.img_list) - 1:
                self.animation_count += 1
                self.img = self.img_list[math.floor(self.animation_count)]
            else:
                self.pop = True

        if self.pop:
            return self.rect_img.y
        else:
            return None


class CameraThread:
    def __init__(self, width=1280, height=720):
        self.cap = None
        self.frame = None
        self.running = False
        self.lock = threading.Lock()
        self.camera_ready = False
        self.width = width
        self.height = height

        # Start camera initialization in separate thread
        self.init_thread = threading.Thread(target=self._init_camera, daemon=True)
        self.init_thread.start()

    def _init_camera(self):
        """Initialize camera in separate thread"""
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.width)
        self.cap.set(4, self.height)

        # Warm up camera by reading a few frames
        for _ in range(5):
            self.cap.read()

        self.camera_ready = True
        self.running = True
        self._capture_loop()

    def _capture_loop(self):
        """Continuously capture frames in background"""
        while self.running:
            if self.cap and self.cap.isOpened():
                success, img = self.cap.read()
                if success:
                    with self.lock:
                        self.frame = cv2.flip(img, 1)

    def get_frame(self):
        """Get the latest frame"""
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def is_ready(self):
        """Check if camera is ready"""
        return self.camera_ready

    def release(self):
        """Release camera resources"""
        self.running = False
        if self.cap:
            self.cap.release()


def game():
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
    img_score = pygame.image.load("../../Resources/Project - Balloon Pop/BackgroundScore.png").convert_alpha()

    # buttons
    back_button = ButtonImg((578, 450), "../../Resources/Project - Balloon Pop/ButtonBack.png",
                            path_hover_sound="../../Resources/Sounds/hover.mp3",
                            path_click_sound="../../Resources/Sounds/click.mp3",
                            scale=0.5)

    # load background music
    pygame.mixer.pre_init()
    pygame.mixer.music.load("../../Resources/Project - Balloon Pop/BackgroundMusicGame.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

    # initialize camera thread (non-blocking)
    camera = CameraThread(width, height)

    # variables
    balloons = []
    start_time = None
    generator_start_time = None
    time_interval = 1
    speed = 5
    score = 0
    total_time = 40
    game_started = False

    # create hand detector
    detector = HandDetector(maxHands=1, detectionCon=0.8)

    # get all balloon paths
    path_balloon_folder = "../../Resources/Project - Balloon Pop/Balloons/"
    path_list_balloons = os.listdir(path_balloon_folder)

    # Create a placeholder surface for when camera isn't ready
    placeholder_surface = pygame.Surface((width, height))
    placeholder_surface.fill((50, 50, 50))
    font = pygame.font.Font("../../Resources/Marcellus-Regular.ttf", 40)
    loading_text = font.render("Initializing Camera...", True, (255, 255, 255))
    loading_rect = loading_text.get_rect(center=(width // 2, height // 2))

    # balloon generator
    def generate_balloon():
        random_balloon_path = path_list_balloons[random.randint(0, len(path_list_balloons) - 1)]
        # Use a default y position if camera frame isn't ready yet
        y = height
        x = random.randint(100, width - 100)
        random_scale = round(random.uniform(0.3, 0.7), 2)

        balloons.append(Balloon((x, y), path=os.path.join(path_balloon_folder, random_balloon_path),
                                grid=(3, 4), scale=random_scale, speed=speed,
                                path_sound_pop="../../Resources/Project - Balloon Pop/Pop.wav"))

    # main loop
    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                camera.release()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    camera.release()
                    Scene_manager.open_scene("Menu")

        # check for time remaining
        if not game_started:
            if camera.is_ready():
                game_started = True
                start_time = time.time()
                generator_start_time = time.time()
            time_remaining = total_time
        else:
            time_remaining = total_time - (time.time() - start_time)

        if time_remaining < 0:
            window.blit(img_score, (0, 0))
            font = pygame.font.Font("../../Resources/Marcellus-Regular.ttf", 70)
            text_score = font.render(f"Score: {score}", True, (0, 0, 200))
            text_score_rect = text_score.get_rect(center=(1280 / 2, 720 / 2))
            window.blit(text_score, text_score_rect)

            # button to go back
            back_button.draw(window)
            if back_button.state == "click":
                pygame.mixer.music.stop()
                camera.release()
                Scene_manager.open_scene("Menu")

        else:
            # Get frame from camera thread
            img = camera.get_frame()

            if img is not None and camera.is_ready():
                # Process frame with hand detector
                hands, img = detector.findHands(img, draw=False, flipType=False)

                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                imgRGB = np.rot90(imgRGB)
                frame = pygame.surfarray.make_surface(imgRGB).convert()
                frame = pygame.transform.flip(frame, True, False)
                window.blit(frame, (0, 0))

                # check for detected hands
                if hands:
                    hand = hands[0]
                    x, y = hand['lmList'][8][:2]
                    pygame.draw.circle(window, (0, 0, 200), (x, y), 20)
                    pygame.draw.circle(window, (200, 200, 200), (x, y), 16)
                else:
                    x, y = 0, 0
            else:
                # Show loading screen while camera initializes
                window.blit(placeholder_surface, (0, 0))
                window.blit(loading_text, loading_rect)
                x, y = 0, 0

            # loop through the balloons and draw them
            for i, balloon in enumerate(balloons):
                if balloon:
                    balloon_score = balloon.check_pop(x, y)
                    if balloon_score:
                        score += balloon_score // 10
                        balloons[i] = False
                    balloon.draw(window)

            # Only generate balloons and update game logic if game has started
            if game_started and time.time() - generator_start_time > time_interval:
                time_interval = random.uniform(0.3, 0.8)
                generate_balloon()
                generator_start_time = time.time()
                speed += 1

            # add text for score and time
            font = pygame.font.Font("../../Resources/Marcellus-Regular.ttf", 45)
            text_score = font.render(f"Score: {score}", True, (200, 200, 200))
            text_time = font.render(f"Time: {int(time_remaining)}", True, (200, 200, 200))
            pygame.draw.rect(window, (200, 0, 200), (10, 10, 300, 70), border_radius=20)
            pygame.draw.rect(window, (200, 0, 200), (950, 10, 300, 70), border_radius=20)
            window.blit(text_score, (40, 13))
            window.blit(text_time, (1000, 13))

        # update display
        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    game()