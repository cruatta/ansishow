import pygame
import sys


def calc_x_y(_screen, _graphic_x):
    return _screen.get_size()[0] / 2 - _graphic_x / 2, _screen.get_size()[1]


def load_image(path: str):
    img = pygame.image.load(path)
    img_x, img_y = img.get_size()
    return img, img_x, img_y


pygame.init()
graphic = pygame.image.load(sys.argv[1])
graphic_x, graphic_y = graphic.get_size()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = 1
x, y = screen.get_size()[0] / 2 - graphic_x / 2, screen.get_size()[1]

background = pygame.surface.Surface((screen.get_width(), screen.get_height()))
background.fill((0, 0, 0))


while running:
    clock.tick(60)
    for event in pygame.event.get():  # get user input
        if event.type == pygame.QUIT:  # if user clicks the close X
            running = 0  # make running 0 to break out of loop
        if event.type == pygame.KEYDOWN:
            y -= 100
            screen.blit(graphic, (x, y))
            pygame.display.flip()
    screen.blit(background, (0, 0))
    screen.blit(graphic, (x, y))
    pygame.display.flip()  # Update screen
    y -= 1

    if y < -graphic_y - 100:
        graphic, graphic_x, graphic_y = load_image('test.png')
        x, y = calc_x_y(screen, graphic_x)



