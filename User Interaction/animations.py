import pygame
import math



# initiate pygame
pygame.init()

# create window
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animations")

# initialize clock for FPS
fps = 30
clock = pygame.time.Clock()

# variables
counter = 0

class Dinosaur:
    def __init__(self, pos, path, scale=1, grid=(2, 4),
                 animation_frames=None, animation_speed=1):

        # load images
        img = pygame.image.load(path).convert_alpha()
        width, height = img.get_size()
        img = pygame.transform.smoothscale(img, (int(width * scale), int(height * scale)))


        # split images to get frames
        if animation_frames is None:
            animation_frames = grid[0] * grid[1]
        width_single_frame = width / grid[1]
        height_singe_frame = height / grid[0]

        self.img_list = []
        counter = 0

        for row in range(grid[0]):
            for col in range(grid[1]):
                counter += 1
                if counter <= animation_frames:
                    img_crop = img.subsurface((col * width_single_frame, row * height_singe_frame,
                                                   width_single_frame, height_singe_frame))
                    self.img_list.append(img_crop)

        self.img = self.img_list[0]
        self.rect_img = self.img.get_rect()
        self.rect_img.x, self.rect_img.y = pos[0], pos[1]
        self.pos = pos
        self.path = path
        self.animation_count = 0
        self.animation_speed = animation_speed
        self.is_animating = False

    def draw(self, window):
        if self.is_animating:

            if math.floor(self.animation_count) != len(self.img_list) - 1:
                self.animation_count += self.animation_speed
            else:
                self.animation_count = 0

            self.img = self.img_list[math.floor(self.animation_count)]
        else:
            self.img = self.img_list[0]
        window.blit(self.img, self.rect_img)


# create objects of character
dino1 = Dinosaur((100, 100), "../Resources/Animations/DinosaurRun.png",
                 animation_speed=1)
dino2 = Dinosaur((400, 100), "../Resources/Animations/DinosaurWalk.png",
                 grid=(3, 4), animation_frames=10, animation_speed=0.5)
dino3 = Dinosaur((100, 400), "../Resources/Animations/DinosaurJump.png",
                 grid=(3, 4), animation_speed=0.25)
dino4 = Dinosaur((400, 400), "../Resources/Animations/DinosaurDead.png",
                 grid=(3, 4), animation_frames=8, animation_speed=0.5)


# main loop
start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    window.fill((255, 255, 255))
    dino1.draw(window)
    dino2.draw(window)
    dino3.draw(window)
    dino4.draw(window)

    counter += 1
    if counter > 50:
        dino1.is_animating = not dino1.is_animating
        counter = 0

    pygame.display.update()

    clock.tick(fps)
