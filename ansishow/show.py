import math
import pygame
import sys
from images import Images
from dataclasses import dataclass


@dataclass
class ScreenSize:
    width: int
    height: int

    @staticmethod
    def from_size(xy: (int, int)):
        return ScreenSize(xy[0], xy[1])


class ScreenConfig:
    def __init__(self, screen_size: ScreenSize):
        self.next_graphic_offset = screen_size.height / 30
        self.paginate_offset = screen_size.height / 10
        self.scroll_offset = 1

    def inc_scroll_offset(self):
        if self.scroll_offset < 10:
            self.scroll_offset += 1

    def dec_scroll_offset(self):
        if self.scroll_offset > 0:
            self.scroll_offset -= 1


def calc_image_xy(screen_size: ScreenSize, _graphic_width: int) -> (int, int):
    """
    Calculate the placement of an image in the center x of the screen
    :returns:
        (x: int, y: int)
    """
    return screen_size.width / 2 - _graphic_width / 2, screen_size.height


def load_image(screen_size: ScreenSize, path: str) -> (pygame.Surface, int, int):
    """
    Loads an image and returns it as a surface, and it's width and height
    :returns:
        (image: pygame.Surface, width: int, height: int)
    """
    img = pygame.image.load(path)
    img_width, img_height = img.get_size()
    screen_width = screen_size.width
    if img_width > screen_width:
        proportion: float = screen_width / img_width
        new_height: int = math.floor(img_height * proportion)

        img = pygame.transform.scale(img, (screen_width, new_height))
        img_width = screen_width
        img_height = new_height
    return img, img_width, img_height


def run():
    pygame.init()
    if len(sys.argv) < 2:
        print("Missing arguments")
        sys.exit(1)

    if len(sys.argv) == 3 and sys.argv[2] == "--window":
        screen = pygame.display.set_mode((640, 480))
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    running = 1

    print(f"Screen (width, height): {screen.get_size()}")

    screen_size = ScreenSize.from_size(screen.get_size())
    screen_config = ScreenConfig(screen_size)

    ansis = Images(sys.argv[1])

    graphic, graphic_width, graphic_height = load_image(screen_size, ansis.next_image())
    x, y = calc_image_xy(screen_size, graphic_width)

    background = pygame.surface.Surface((screen.get_width(), screen.get_height()))
    background.fill((0, 0, 0))

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = 0
                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    screen_config.inc_scroll_offset()
                if event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                    screen_config.dec_scroll_offset()
                if event.key == pygame.K_r:
                    ansis.reload()
                    print("Reloaded")
                if event.key == pygame.K_TAB:
                    ansis.randomize()
                    print("Randomized")
                if event.key == pygame.K_DOWN:
                    y -= screen_config.paginate_offset
                if event.key == pygame.K_UP:
                    y += screen_config.paginate_offset
                if event.key == pygame.K_PAGEUP or event.key == pygame.K_PAGEDOWN:
                    if event.key == pygame.K_PAGEDOWN:
                        next_image = ansis.next_image()
                    else:
                        next_image = ansis.prev_image()
                    graphic, graphic_width, graphic_height = load_image(
                        screen_size, next_image
                    )
                    next_x, next_y = calc_image_xy(screen_size, graphic_width)
                    x, y = next_x, next_y + screen_config.next_graphic_offset
        screen.blit(background, (0, 0))
        screen.blit(graphic, (x, y))
        pygame.display.flip()
        y -= screen_config.scroll_offset

        if y < -graphic_height - screen_config.next_graphic_offset:
            screen.fill((0, 0, 0))
            next_image = ansis.next_image()
            graphic, graphic_width, graphic_height = load_image(
                ScreenSize.from_size(screen.get_size()), next_image
            )
            x, y = calc_image_xy(screen_size, graphic_width)
