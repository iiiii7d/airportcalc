# airportcalc v1.0.0 - by i____7d
# be sure to read the readme first :^)

import requests
from io import BytesIO
from PIL import Image
import time
import math

def msToTime(ms):
    if ms == 0:
        return "0ms"
    s = math.floor(ms / 1000)
    ms = round(ms % 1000, 2)
    m = math.floor(s / 60)
    s = s % 60
    h = math.floor(m / 60)
    m = m % 60
    d = math.floor(h / 24)
    h = h % 24
    res = ""
    if d != 0:
        res = res + str(d) + "d "
    if h != 0:
        res = res + str(h) + "h "
    if m != 0:
        res = res + str(m) + "min "
    if s != 0:
        res = res + str(s) + "s "
    if ms != 0:
        res = res + str(ms) + "ms "
    return res.strip()

while True:
    url = input("Image URL: ")
    if url.endswith(".png") or url.endswith(".jpg"):
        break
    else:
        print("Your URL needs to end with either .png or .jpg.")

def removenegativesign(string):
    if string.startswith("-"):
        return string[1:]
    else:
        return string

a = input("Do you want measurements in blocks & km^2? (y/n): ")
if a == "y":
    while True:
        westx = input("Western X coord on map: ")
        if removenegativesign(westx).isdigit():
            westx = int(westx)
            break
        else:
            print("Please put in a number.")
    while True:
        eastx = input("Eastern X coord on map: ")
        if removenegativesign(eastx).isdigit():
            eastx = int(eastx)
            break
        else:
            print("Please put in a number.")
    while True:
        northz = input("Northern Z coord on map: ")
        if removenegativesign(northz).isdigit():
            northz = int(northz)
            break
        else:
            print("Please put in a number.")
    while True:
        southz = input("Southern Z coord on map: ")
        if removenegativesign(southz).isdigit():
            southz = int(southz)
            break
        else:
            print("Please put in a number.")

    actualsize = (eastx - westx) * (southz - northz)

r = requests.get(url)
i = Image.open(BytesIO(r.content))
pmap = i.load()
size = i.size[0] * i.size[1]
rgb = i.convert("RGB")
reds = 0
greens = 0
count = 0
start = int(round(time.time() * 1000))

def addzeroes(string):
    if not "." in string:
        return string + ".00"
    elif len(string.split(".")[1]) == 1:
        return string + "0"
    else:
        return string

for x in range(i.size[0]):
    for y in range(i.size[1]):
        if rgb.getpixel((x,y)) == (255, 0, 0):
            reds += 1
        elif rgb.getpixel((x,y)) == (0, 255, 0):
            greens += 1
        count += 1
        timeLeft = round(((int(round(time.time() * 1000)) - start) / count * (size - count)), 2)
        print("Scanned pixel " + str(count) + " of " + str(size) + " (" + addzeroes(str(round(count/size*100, 2))) + "%, check back in " + msToTime(timeLeft) + ")")

try:
    print("Scan complete in " + msToTime(int(round(time.time() * 1000)) - start))
    print("The airport space is " + str(round(greens/reds*100, 2)) + "% of your city.")
    if a == "y":
        print("Your city's land area is " + str(round(reds/size * actualsize, 2)) + " blocks (" + str(round(reds/size * actualsize / 1000000, 2)) + "km^2)")
        print("Your airport space's land area is " + str(round(greens/size * actualsize, 2)) + " blocks (" + str(round(greens/size * actualsize / 1000000, 2)) + "km^2)")
        print("You have " + str(round(reds/size * actualsize - greens/size * actualsize, 2)) + " blocks of airport space left.")
    print("Note that these values may or may not be accurate, depending on how you marked the areas out.")
except ZeroDivisionError:
    print("There are no solid red pixels in the picture!")

end = input()
