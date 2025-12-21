from PIL import Image

def is_image_grayscale(img: Image.Image) -> bool:
    img = img.convert("RGB")
    for r, g, b in img.getdata():
        if r != g or g != b:
            return False
    return True
