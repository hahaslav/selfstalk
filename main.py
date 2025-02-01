from mss.windows import MSS as mss
from PIL import Image

def take_screenshot():
    with mss() as sct:
        new_screenshot = sct.grab(sct.monitors[0])
    return Image.frombytes("RGB", new_screenshot.size, new_screenshot.bgra, "raw", "BGRX")

def resize_image(image, new_height):
    new_width = new_height * image.width // image.height
    return image.resize((new_width, new_height), Image.Resampling.BOX)

if __name__ == '__main__':
    screenshot = resize_image(take_screenshot(), 540)