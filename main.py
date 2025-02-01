from mss.windows import MSS as mss
from PIL import Image
import base64
import requests

def take_screenshot():
    with mss() as sct:
        new_screenshot = sct.grab(sct.monitors[0])
    return Image.frombytes("RGB", new_screenshot.size, new_screenshot.bgra, "raw", "BGRX")

def resize_image(image, new_height):
    new_width = new_height * image.width // image.height
    return image.resize((new_width, new_height), Image.Resampling.BOX)

def make_data_string():
    with open("screenshots/1.png", 'rb') as fin:
        image = fin.read()
    return f"data:image/png;base64,{base64.b64encode(image).decode("utf-8")}"

def chat(image_data_string):
    response = requests.post(
        "http://127.0.0.1:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "minicpm-v-2_6",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "This is a screenshot. What is this user doing?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_data_string}
                        }
                    ]
                }
            ],
            "stream": False
        }
    ).json()

    return response["choices"][0]["message"]["content"]

if __name__ == '__main__':
    screenshot = resize_image(take_screenshot(), 540)
    screenshot.save("screenshots/1.png")
    print(chat(make_data_string()))