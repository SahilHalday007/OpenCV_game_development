import cv2
import numpy as np
import pygame
import random as r
from cvzone.HandTrackingModule import HandDetector
import time


# initialize and set pygame window
pygame.init()
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Pop")

fps = 30
clock = pygame.time.Clock()

# set videocam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# load images
imgBalloon = pygame.image.load('../Resources/Project - Balloon Pop/Balloons/BalloonRed.png').convert_alpha()
rectBalloon = imgBalloon.get_rect()
rectBalloon.x, rectBalloon.y = 500, 300

# variables
speed = 20
score = 0
start_time = time.time()
total_time = 5

# create detector
detector = HandDetector(detectionCon=0.8, maxHands=1)


def reset_balloon():
    rectBalloon.x = r.randint(100, img.shape[0] - 100)
    rectBalloon.y = img.shape[0] + 50



# main loop
start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # apply logic
    time_remaining = int(total_time - (time.time() - start_time))

    if time_remaining < 0:
        window.fill((255, 255, 255))

        font = pygame.font.Font('../Resources/Marcellus-Regular.ttf', 50)
        text_score = font.render(f" Your Score: {score}", True, (50, 50, 250))
        text_time = font.render(f" Time is UP", True, (50, 50, 250))
        window.blit(text_score, (450, 350))
        window.blit(text_time, (530, 275))

    else:
        # OpenCV
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        rectBalloon.y -= speed # move the balloon up

        # check if balloon reached top
        if rectBalloon.y  < 0:
            reset_balloon()
            speed += 1


        if hands:
            hand = hands[0]
            x, y = hand['lmList'][8][:2]
            if rectBalloon.collidepoint(x, y):
                reset_balloon()
                score += 10
                speed += 1



        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        window.blit(imgBalloon, rectBalloon)

        font = pygame.font.Font('../Resources/Marcellus-Regular.ttf', 50)
        text_score = font.render(f" Score: {score}", True, (50, 50, 250))
        text_time = font.render(f" Time: {time_remaining}", True, (50, 50, 250))
        window.blit(text_score, (35, 35))
        window.blit(text_time, (1000, 35))


    # update display
    pygame.display.update()
    clock.tick(fps)



