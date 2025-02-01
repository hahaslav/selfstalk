from mss.windows import MSS as mss
from PIL import Image

def take_screenshot():
    with mss() as sct:
        new_screenshot = sct.grab(sct.monitors[0])
        return Image.frombytes("RGB", new_screenshot.size, new_screenshot.bgra, "raw", "BGRX")

if __name__ == '__main__':
    screenshot = take_screenshot()