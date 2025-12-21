import numpy as np
from PIL import Image

def is_image_grayscale(img: Image.Image) -> bool:
    img = img.convert("RGB")

    arr = np.asarray(img)

    # compare image colors
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    return np.array_equal(r, g) and np.array_equal(g, b)
