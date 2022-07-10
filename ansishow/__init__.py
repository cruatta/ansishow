import pygame
import sys
from typing import List
from pathlib import Path


def get_image_paths(base_path: str) -> List[str]:
    """

    :param base_path:
    :return:
    """
    def path_str(each: Path) -> str:
        return str(each)

    path = Path(base_path)
    img_paths = path.glob('**/*.png')
    return list(map(path_str, list(img_paths)))


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

image_paths = get_image_paths(sys.argv[1])
if len(image_paths) < 1:
    sys.exit(1)

img_idx = 0

graphic, graphic_width, graphic_height = load_image(image_paths[img_idx])
x, y = calc_image_xy(screen, graphic_width)

background = pygame.surface.Surface((screen.get_width(), screen.get_height()))
background.fill((0, 0, 0))


while running:
    clock.tick(60)
    for event in pygame.event.get():  # get user input
        if event.type == pygame.QUIT:  # if user clicks the close X
            running = 0  # make running 0 to break out of loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                y -= 100
                screen.blit(graphic, (x, y))
                pygame.display.flip()
    screen.blit(background, (0, 0))
    screen.blit(graphic, (x, y))
    pygame.display.flip()  # Update screen
    y -= 1

    if y < -graphic_height - 50:
        img_idx += 1

        if img_idx == len(image_paths):
            img_idx = 0
        else:
            graphic, graphic_width, graphic_height = load_image(image_paths[img_idx])
            x, y = calc_image_xy(screen, graphic_width)
