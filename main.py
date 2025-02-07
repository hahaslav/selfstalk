from mss.windows import MSS as mss
from PIL import Image
import base64
from datetime import datetime
import asyncio
import aiohttp
import os

LMS_SERVER = "http://127.0.0.1:1234"
LLM = "minicpm-v-2_6"

def take_screenshot():
    with mss() as sct:
        new_screenshot = sct.grab(sct.monitors[0])
    return Image.frombytes("RGB", new_screenshot.size, new_screenshot.bgra, "raw", "BGRX")

def resize_image(image, new_height):
    new_width = new_height * image.width // image.height
    return image.resize((new_width, new_height), Image.Resampling.BOX)

def make_data_string(filename):
    with open(filename, 'rb') as fin:
        image = fin.read()
    return f"data:image/png;base64,{base64.b64encode(image).decode("utf-8")}"

async def chat(image_data_string):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{LMS_SERVER}/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": LLM,
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
        ) as response:
            return await response.json()

def write_history(text, history_path):
    with open(history_path, 'a', encoding="UTF-8") as fout:
        fout.write(text)

def main(history_time):
    shot_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    screenshot = resize_image(take_screenshot(), 540)
    if not os.path.exists("screenshots"):
        os.mkdir("screenshots")
    if not os.path.exists("history"):
        os.mkdir("history")
    image_path = f"screenshots/{shot_time}.png"
    history_path = f"history/{history_time}.txt"
    screenshot.save(image_path)
    description = f"{shot_time}\n{asyncio.run(chat(make_data_string(image_path)))["choices"][0]["message"]["content"]}\n\n"
    print(description)
    write_history(description, history_path)

if __name__ == "__main__":
    history_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    try:
        while True:
            main(history_time)
    except KeyboardInterrupt:
        print("The logging is now stopped. The last screenshot was saved without its corresponding description. But the LLM continues to work.")
