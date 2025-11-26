import pygame
import cv2
import cvzone
import numpy as np

pygame.init()

width, height = 1280, 720

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My awesome game")

fps = 30
clock = pygame.time.Clock()

# web cam
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # width
cap.set(4, 720) # height

start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # opencv
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)

    window.blit(frame, (0, 0))

    pygame.display.update()

    clock.tick(fps)
