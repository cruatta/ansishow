import pygame
import sys
from ansi import ANSI


def calc_image_xy(_screen: pygame.display, _graphic_width: int) -> (int, int):
    """
    Calculate the placement of an image in the center x of the screen
    :returns:
        (x: int, y: int)
    """
    return _screen.get_size()[0] / 2 - _graphic_width / 2, _screen.get_size()[1]


def load_image(path: str) -> (pygame.Surface, int, int):
    """
    Loads an image and returns it as a surface, and it's width and height
    :returns:
        (image: pygame.Surface, width: int, height: int)
    """
    img = pygame.image.load(path)
    img_width, img_height = img.get_size()
    return img, img_width, img_height


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = 1

NEXT_GRAPHIC_OFFSET = screen.get_size()[1] / 30
SCROLL_OFFSET = screen.get_size()[1] / 10

ansis = ANSI(sys.argv[1])

graphic, graphic_width, graphic_height = load_image(ansis.next_image())
x, y = calc_image_xy(screen, graphic_width)

background = pygame.surface.Surface((screen.get_width(), screen.get_height()))
background.fill((0, 0, 0))


while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                y -= SCROLL_OFFSET
            if event.key == pygame.K_UP:
                y += SCROLL_OFFSET
            if event.key == pygame.K_SPACE:
                next_image = ansis.next_image()
                graphic, graphic_width, graphic_height = load_image(next_image)
                next_x, next_y = calc_image_xy(screen, graphic_width)
                x, y = next_x, next_y + NEXT_GRAPHIC_OFFSET
    screen.blit(background, (0, 0))
    screen.blit(graphic, (x, y))
    pygame.display.flip()
    y -= 1

    if y < -graphic_height - NEXT_GRAPHIC_OFFSET:
        next_image = ansis.next_image()
        graphic, graphic_width, graphic_height = load_image(next_image)
        x, y = calc_image_xy(screen, graphic_width)
