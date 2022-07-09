import pygame
import sys

pygame.init()
graphic = pygame.image.load(sys.argv[1])
graphic_x, graphic_y = graphic.get_size()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
running = 1
x, y = screen.get_size()[0] / 2 - graphic_x / 2, screen.get_size()[1]


# WIP
class ANSI(pygame.sprite.Sprite):
    def __init__(self, image_file, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


while running:
    clock.tick(60)
    for event in pygame.event.get():  # get user input
        if event.type == pygame.QUIT:  # if user clicks the close X
            running = 0  # make running 0 to break out of loop
        if event.type == pygame.KEYDOWN:
            y -= 100
            screen.blit(graphic, (x, y))
            pygame.display.flip()
    screen.blit(graphic, (x, y))
    pygame.display.flip()  # Update screen
    y -= 1

