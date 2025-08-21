import math
from typing import Tuple

import pygame
from ansishow.images import Images
from dataclasses import dataclass
from argparse import ArgumentParser


@dataclass
class ScreenSize:
    width: int
    height: int

    @staticmethod
    def from_size(xy: Tuple[int, int]):
        return ScreenSize(xy[0], xy[1])


class ScreenConfig:
    def __init__(self, screen_size: ScreenSize, scaled: bool):
        self.screen_size = screen_size
        self.scaled = scaled
        self.next_graphic_offset = screen_size.height / 30
        self.paginate_offset = screen_size.height / 10
        self.scroll_offset = 1

    def inc_scroll_offset(self):
        if self.scroll_offset < 10:
            self.scroll_offset += 1

    def dec_scroll_offset(self):
        if self.scroll_offset > 0:
            self.scroll_offset -= 1


def calc_image_xy(screen_size: ScreenSize, _graphic_width: int) -> Tuple[float, int]:
    """
    Calculate the placement of an image in the center x of the screen
    :returns:
        (x: float, y: int)
    """
    return screen_size.width / 2 - _graphic_width / 2, screen_size.height


def load_image(screen_config: ScreenConfig, path: str) -> Tuple[pygame.Surface, int, int]:
    """
    Loads an image and returns it as a surface, and it's width and height
    :returns:
        (image: pygame.Surface, width: int, height: int)
    """
    img = pygame.image.load(path)
    img_width, img_height = img.get_size()
    screen_width = screen_config.screen_size.width
    if img_width > screen_width or screen_config.scaled:
        proportion: float = screen_width / img_width
        new_height: int = math.floor(img_height * proportion)

        img = pygame.transform.scale(img, (screen_width, new_height))
        img_width = screen_width
        img_height = new_height
    return img, img_width, img_height


def run():
    pygame.init()

    joystick_count = pygame.joystick.get_count()
    if joystick_count == 1:
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    args = ArgumentParser()
    args.add_argument("path", type=str)
    args.add_argument("--window", type=bool, const=True, default=False, nargs="?")
    args.add_argument("--scaled", type=bool, const=True, default=False, nargs="?")
    args.add_argument('--rotate', type=int, choices=[0, 90, 180, 270], default=0, nargs="?")
    config = args.parse_args()

    if config.window:
        screen = pygame.display.set_mode((640, 480))
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    running = 1

    print(f"Screen (width, height): {screen.get_size()}")

    # Handle rotation - create render surface with appropriate dimensions
    screen_width, screen_height = screen.get_size()
    if config.rotate in [90, 270]:
        # Swap dimensions for 90/270 degree rotations
        render_size = (screen_height, screen_width)
    else:
        render_size = (screen_width, screen_height)
    
    render_surface = pygame.surface.Surface(render_size)
    
    screen_size = ScreenSize.from_size(render_size)
    screen_config = ScreenConfig(screen_size, config.scaled)

    ansis = Images(config.path)

    graphic, graphic_width, graphic_height = load_image(
        screen_config, ansis.next_image()
    )
    x, y = calc_image_xy(screen_size, graphic_width)

    background = pygame.surface.Surface(render_size)
    background.fill((0, 0, 0))

    alert_font = pygame.font.SysFont("Arial", 30)

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
            if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
                if(event.type == pygame.JOYBUTTONDOWN):
                    button_num = event.button
                    button_name = f"Button {button_num}"
                    alert_surface = alert_font.render(f'Pressed {button_name}', True, (255, 255, 255))
                    alert_rect = alert_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                    screen.blit(alert_surface, alert_rect)
                    pygame.display.flip()
                if event.key == pygame.K_ESCAPE:
                    running = 0
                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    screen_config.dec_scroll_offset()
                if event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                    screen_config.inc_scroll_offset()
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
                        screen_config, next_image
                    )
                    next_x, next_y = calc_image_xy(screen_size, graphic_width)
                    x, y = next_x, next_y + screen_config.next_graphic_offset

        # Render to the render surface
        render_surface.blit(background, (0, 0))
        render_surface.blit(graphic, (x, y))
        
        # Apply rotation and blit to actual screen
        if config.rotate != 0:
            rotated_surface = pygame.transform.rotate(render_surface, config.rotate)
            # Center the rotated surface on the screen
            rot_rect = rotated_surface.get_rect(center=(screen_width//2, screen_height//2))
            screen.fill((0, 0, 0))  # Clear screen first
            screen.blit(rotated_surface, rot_rect)
        else:
            screen.blit(render_surface, (0, 0))
            
        pygame.display.flip()
        y -= screen_config.scroll_offset

        if y < -graphic_height - screen_config.next_graphic_offset:
            render_surface.fill((0, 0, 0))
            next_image = ansis.next_image()
            graphic, graphic_width, graphic_height = load_image(
                screen_config, next_image
            )
            x, y = calc_image_xy(screen_size, graphic_width)
