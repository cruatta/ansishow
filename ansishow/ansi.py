from typing import List
from pathlib import Path
from random import shuffle


class ANSI:
    def __init__(self, path: str):
        self.path = path
        self.image_paths = ANSI.get_image_paths(path)
        if len(self.image_paths) < 1:
            raise ValueError("Invalid Path - No Images")
        self.image_index = 0

    @staticmethod
    def get_image_paths(base_path: str, recursive: bool = False) -> List[str]:
        """
        Gets all pngs in a given base_path, optionally recursive
        :returns:
            List of image paths
        """

        def path_str(each: Path) -> str:
            return str(each)

        path = Path(base_path)
        if recursive:
            img_paths = path.glob("**/*.png")
        else:
            img_paths = path.glob("*.png")
        return list(map(path_str, list(img_paths)))

    def reload(self):
        self.image_index = 0
        self.image_paths = ANSI.get_image_paths(self.path)

    def next_image(self) -> str:
        self.image_index += 1
        if self.image_index == len(self.image_paths):
            self.reload()
        return self.image_paths[self.image_index]

    def randomize(self):
        shuffle(self.image_paths)
