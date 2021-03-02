import requests
import time

import os
from dotenv import load_dotenv

load_dotenv()
DEVICE = os.getenv('DEVICE')
TOKEN = os.getenv('TOKEN')

url = 'https://api.particle.io/v1/devices/' + DEVICE + '/led?access_token=' + TOKEN

print(url)

on = {'value': 'on'}
off = {'value': 'off'}

morse = {'a':'._','b':'_...','c':'_._.','d':'_...','e':'.','f':'.._.',
            'g':'__.','h':'....','i':'..','j':'.___','k':'_._','l':'._..',
            'm':'__','n':'_.','o':'___','p':'.__.','q':'__._','r':'._.',
            's':'...','t':'_','u':'.._','v':'..._','w':'.__','x':'_.._',
            'y':'_.__','z':'__..','1':'.____','2':'..___','3':'...__',
            '4':'...._','5':'.....','6':'_....','7':'__...','8':'___..',
            '9':'____.','0':'_____','.':'._._._',',':'__..__','?':'..__..',
            ' ':''}

dotlength = 1
dashlength = 3 # a dash equals 3 dots
wordgap = 7
chargap = 3

# characteristic flashing time (s)
tau = 0.3

message = input('What would you like to send to meme?\n').lower()

print('You entered: ' + message)

# check if sentence is legal or not
for c in message:
    try:
        morse[c]
    except:
        print('Char \"' + str(c) + '\" not recognized for morse')
        exit()

morseseq = ''

for c in message:
    if not c == ' ':
        morseseq = morseseq + morse[c] + 'c'
    else:
        morseseq = morseseq + 'w'

print('Your message in morse is: ' + morseseq)

lightseq = ''

for c in morseseq:
    if c == '.':
        lightseq = lightseq + dotlength * '1' + dotlength * '0'
    elif c == '_':
        lightseq = lightseq + dashlength * '1' + dotlength * '0'
    elif c == 'c':
        # a . or _ precedes c, so do less 0's
        lightseq = lightseq + (chargap - dotlength) * '0'
    elif c == 'w':
        # c must precede w, so do less 0's
        lightseq = lightseq + (wordgap - chargap) * '0'
    else:
        print("lmao something broke this shouldn't happen")

i = len(lightseq) - 1

# remove trailing 0's commands
while i > 0:
    if not lightseq[i] == '1':
        i = i - 1
    else:
        break

# idk why I need to +1 here, i'm tired and not trying to think also turn it off as the last command
lightseq = lightseq[0:i + 1] + '0'

print("Sending data:" + lightseq)

# now let's take 0's and 1's and send to lamp, but be smart
current = None
for c in lightseq:
    if c == '1':
        if not current == '1':
            print(requests.post(url, data = on).text)
            current = '1'
        else:
            print("current state already 1")
    else:
        if not current == '0':
            print(requests.post(url, data = off).text)
            current = '0'
        else:
            print("current state already 0")
    time.sleep(tau)

print("Data transfer complete")