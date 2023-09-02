import os, discord
import random, shutil
import asyncio, requests
from PIL import Image
from dotenv import load_dotenv as load
load()
styles = {
    "default": "text2img",
    "Cute Animal": "cute-creature-generator",
    "Fantasy World": "fantasy-world-generator",
    "Cyberpunk": "cyberpunk-generator",
    "Anime Portrait": "anime-portrait-generator",
    "3D Objects": "3d-objects-generator",
    "3D Origami": "origami-3d-generator",
    "3D Hologram": "hologram-3d-generator",
    "3D Character": "3d-character-generator",
    "Watercolor": "watercolor-painting-generator",
    "Pop Art": "pop-art-generator",
    "Architecture": "contemporary-architecture-generator",
    "Futuristic Architecture": "future-architecture-generator",
    "Watercolor Architecture": "watercolor-architecture-generator",
    "Fantasy Character": "fantasy-character-generator",
    "Steampunk": "steampunk-generator",
    "Pixel Art": "pixel-art-generator",
    "Street Art": "street-art-generator",
    "Surreal Portrait": "surreal-portrait-generator",
    "Anime World": "anime-world-generator",
    "Fantasy Portrait": "fantasy-portrait-generator",
    "Comic Protrait": "comics-portrait-generator",
    "Cyberpunk Portrait": "cyberpunk-portrait-generator"
}

async def asyncify(func, *args):
    coro = asyncio.to_thread(func, *args)
    task = asyncio.create_task(coro)
    result = await task
    return result

async def generate_from_prompt(prompt, style="default", negative_prompt=""):
    # return "https://images-ext-2.discordapp.net/external/7IPiq6pXLW3JvLeyyx8DX8_qvh-R2J9A5LIPbmUdWyI/https/api.deepai.org/job-view-file/f659d208-b4af-4a12-845e-f7e2fb6ab4e9/outputs/output.jpg?width=1156&height=1156"
    if style == "default": style = styles[style]
    data = await asyncify(prompt_coro, prompt, style)
    return data

def prompt_coro(prompt, style, negative_prompt=""):
    headers = {
        'api-key': os.getenv("DEEPAI_API_KEY"),
    }

    files = {
        'text': (None, prompt),
    }

    if negative_prompt != "":
        files["negative_prompt"] = (None, negative_prompt)

    response = requests.post(f'https://api.deepai.org/api/{style}', headers=headers, files=files)
    print(response.json())
    return response.json()['output_url']

def crop_quadrant(url, quadrant):
    file = f"{random.randint(1,10000)}.jpg"
    response = requests.get(url, stream=True)
    with open(file, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    img = Image.open(file)
    if quadrant == 1:
        #top-left quadrant
        cropped_img = img.crop((0, 0, 512, 512))
    elif quadrant == 2:
        #top-right quadrant
        cropped_img = img.crop((512, 0, 1024, 512))
    elif quadrant == 3:
        #bottom-left quadrant
        cropped_img = img.crop((0, 512, 512, 1024))
    elif quadrant == 4:
        #bottom-right quadrant
        cropped_img = img.crop((512, 512, 1024, 1024))
    os.remove(file)
    cropped_img.save(file)
    return file