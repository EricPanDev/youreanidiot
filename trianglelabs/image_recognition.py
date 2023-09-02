import os
import requests
import random
import asyncio
from threading import Thread
from dotenv import load_dotenv as load
load()
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        try:
            Thread.join(self, timeout=5)
        except: ...
        try:
            return self._return
        except:
            return ""
API_URLS = [
    "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large",
    "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base",
    "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning",
    "https://api-inference.huggingface.co/models/ydshieh/vit-gpt2-coco-en"
]
headers = {"Authorization": os.getenv("HUGGING_FACE_TOKEN")}

def fetch_response(client, api_url, data):
    print("fetching")
    response = client.post(api_url, headers=headers, data=data, timeout=30)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    
    return response.json()[0]['generated_text']

async def asyncify(func, *args):
    coro = asyncio.to_thread(func, *args)
    task = asyncio.create_task(coro)
    result = await task
    return result

async def query(filename):
    print("starting")
    with open(filename, "rb") as f:
        data = f.read()
    responses = []
    client = requests.Session()
    tasks = [ThreadWithReturnValue(target=fetch_response, args=(client, api_url, data,)) for api_url in API_URLS]
    for task in tasks:
        task.start()
    text_in_image = await OCR.raw(data)
    for task in tasks:
        responses.append(task.join())
    data = ""
    for i in responses:
        try:
            data = data + " " + i
        except:
            ...
    # responses = await asyncio.gather(*tasks, return_exceptions=True)

    return data + ". The image contains" + text_in_image

def download_image(image_url, save_as):
    client = requests.Session()
    response = client.get(image_url)
    with open(save_as, "wb") as f:
        f.write(response.content)

async def main():
    await asyncify(download_image, "https://easydrawingart.com/wp-content/uploads/2022/10/How-to-Draw-Donald-Duck1.jpg", "download.png")
    res = await query("download.png")
    print(res)

if __name__ == "__main__":
    asyncio.run(main())

async def image_recognition(url):
    file = random.randint(0, 1000000)
    await asyncify(download_image, url, f"{file}.png")
    res = await query(f"{file}.png")
    os.remove(f"{file}.png")
    return res

class OCR:
        async def raw(raw):
            res = await asyncify(OCR.raw_coro, raw)
            return res
        def raw_coro(raw):
            r = requests.post(
                'https://api.api-ninjas.com/v1/imagetotext',
                files={'image': raw},
                headers={
                    'X-Api-Key':
                    os.getenv("API_NINJAS_KEY")
                }
            )
            res = r.json()
            text = []
            for i in res:
                text.append(i["text"])
            text2 = ' '.join(text)

            return (" the text " + text2.strip()) if text2.strip() != "" else (" no text.")