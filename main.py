#importing the modules(shoutout to PIL tho)
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from geopy.geocoders import Nominatim
import time, requests, json, ctypes, geopy, os

#setting up some variables
apikey = "h"
longitude = 0
latitude = 0
unit = "metric"

#opening up config.txt and changing some stuff
config = open("config.txt")
config = config.read().splitlines()
for i in config:
    exec(i)

#ottawa temperature
#longitude = -75.7464925
#latitude = 45.350048

#getting the weather from openweathermap
weather = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s&units=%s" % (latitude, longitude, apikey, unit))
rawweather = weather.json()

#getting some information from the api
weather = rawweather["weather"][0]["description"].lower()
temperature = rawweather["main"]["temp"]

#figuring out where you are(DOXXING??!!)
geolocator = Nominatim(user_agent = "geoapiExcercises")
location = geolocator.reverse(str(latitude) + "," + str(longitude))

#getting the city(100% DOXXING!!!!!)
try:
    location = location.raw["address"]["city"]
except:
    try:
        location = location.raw["address"]["county"]
    except:
        location = "your city"

#creating the image that will be the wallpaper
together = Image.new("RGBA", (160, 120), (255, 255, 255))

#getting some useful information
month = int(time.strftime("%m"))
hour = int(time.strftime("%H"))
date = time.strftime("%D")

#inefficient code? never heard of it
if(hour < 8):
    stage = 1
elif(hour < 10):
    stage = 2
elif(hour < 12):
    stage = 3
elif(hour < 14):
    stage = 4
elif(hour < 16):
    stage = 5
elif(hour < 18):
    stage = 6
elif(hour < 20):
    stage = 7
else:
    stage = 8

#getting the season
if(month < 4):
    season = "winter"
elif(month < 7):
    season = "spring"
elif(month < 10):
    season = "summer"
else:
    season = "fall"

#opening the images
land = Image.open("base/%s.png" % season).convert("RGBA")
sky = Image.open("base/sky%s.png" % stage).convert("RGBA")
weatherimage = Image.open("base/%s.png" % weather)

#adding the images together
together = Image.alpha_composite(sky, land)
together = Image.alpha_composite(together, weatherimage)

#jank to get the font the right size
together = together.resize((320, 240), Image.NEAREST)

#changing font color on the temperature(based on celcius so)
if(temperature < -10):
    color = "#04b5c9"
elif(temperature < 0):
    color = "#041bc9"
elif(temperature < 10):
    color = "#04c9a5"
elif(temperature < 20):
    color = "#c97404"
else:
    color = "#c90404"

#drawing the informational text
draw = ImageDraw.Draw(together)
draw.text((0, 210), "%s" % (date), fill = color)
draw.text((0, 220), "It is currently %s degrees outside in %s." % (temperature, location), fill = color)

#changing the size to the actual size of the screen
resolution = [ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)]
together = together.resize(resolution, Image.NEAREST)

#creating the image O_O
together.save("wallpaper.png")

#getting the wallpaper path
path = os.getcwd()

#changing the wallpaper(this is where the magic happens)
ctypes.windll.user32.SystemParametersInfoW(20, 0, r"%s\wallpaper.png" % path, 0)
