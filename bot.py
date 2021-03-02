import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
DEVICE = os.getenv('DEVICE')
TOKEN = os.getenv('TOKEN')

url = 'https://api.particle.io/v1/devices/' + DEVICE + '/?access_token=' + TOKEN

myobjon = {'value': 'on'}
myobjoff = {'value': 'off'}

while True:
    print("Lamp on")
    print(requests.post(url, data = myobjon).text)
    time.sleep(5)
    print("Lamp off")
    print(requests.post(url, data = myobjoff).text)
    time.sleep(5)