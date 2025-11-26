import pygame

# initialize pygame
pygame.init()


class Slider:
    def __init__(self, pos, width_slider=500, color=(0, 200, 0), start_value=50,
                 min=0, max=1023, text=True, font_size=50, font_color=(100, 100, 100), font_path=None):
        self.pos = pos
        self.width_slider = width_slider
        self.color = color
        self.value = start_value
        self.min = min
        self.max = max
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.font_color = font_color

        self.rect = pygame.Rect((self.pos[0], self.pos[1] - 10, self.width_slider, 24))


    def convert_value(self, x, min1, max1, min2, max2):

        return int((x - min1) * (max2 - min2) / (max1 - min1) + min2)


    def draw(self, window):

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos): # check for collision
            if pygame.mouse.get_pressed()[0]: # check if left mouse is clicked
                self.value = self.convert_value(mouse_pos[0] - self.pos[0], 0, self.width_slider,
                                                self.min, self.max)
                print(self.value)

        current_width = (self.value / (self.max - self.min)) * self.width_slider

        # pygame.draw.rect(window, (200, 0, 0) ,rect=self.rect)

        pygame.draw.rect(window, (200, 200, 200),
                         (self.pos[0], self.pos[1], self.width_slider, 5))

        pygame.draw.rect(window, self.color,
                         (self.pos[0], self.pos[1], current_width, 5))

        pygame.draw.circle(window, self.color, (self.pos[0] + current_width, self.pos[1] + 3), 12)

        if self.text:
            font = pygame.font.Font(self.font_path, self.font_size)
            text = font.render(str(self.value), True, self.font_color)
            text_rect = text.get_rect()
            # center text
            text_rect.x = self.pos[0] + self.width_slider + 30
            text_rect.centery = self.rect.centery
            window.blit(text, text_rect)



if __name__ == "__main__":
    width, height = 1280, 720

    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My awesome game")

    fps = 30
    clock = pygame.time.Clock()

    # create sliders
    slider1 = Slider((100, 100), color=(255, 0, 0), width_slider=800)


    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

        window.fill((255, 255, 255))
        slider1.draw(window)

        pygame.display.update()

        clock.tick(fps)
