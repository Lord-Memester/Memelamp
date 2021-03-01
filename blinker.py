import requests
import time

url = 'lamp url'
myobjon = {'value': 'on'}
myobjoff = {'value': 'off'}

while True:
    print("Lamp on")
    print(requests.post(url, data = myobjon).text)
    time.sleep(5)
    print("Lamp off")
    print(requests.post(url, data = myobjoff).text)
    time.sleep(5)
