# --------------------------------------------------------------------
# CS Web Scraper
# --------------------------------------------------------------------

import requests as req
from bs4 import BeautifulSoup as bs

print()

# Sets base URL and base pet ID
baseURL = "https://www.chickensmoothie.com/viewpet.php?id="
basePetID = 1

# Sets testing constants
normalPetID = 112516469
offAccountPetID = 324851447
deletedPetID = 334526694
staffPetID = 338838141

# Gets the page and parses it
html = req.get(baseURL + str(normalPetID)).text
page = bs(html, 'html.parser')

# Checks to see if pet exists
exists = page.find("h2") is None
print("Exists: ", exists, "\n")

if(exists):
    # Finds all pet info
    info = page.find("table", attrs = {"class" : "spine"}).select(".r")

    # Finds the owner ID and name
    owner = str(info[0].find("a"))
    start = owner.find("u=") + 2
    end = owner.rfind("&") if (owner.rfind("&") != None) else len(owner) - 1
    ownerID = owner[start : end]

    start = owner.find(">") + 1
    end = owner.rfind("<")
    ownerName = owner[start : end]

    # Finds the img ID
    img = str(page.find("img", attrs = {"id" : "petimg"}))
    start = img.find("?k=") + 3
    end = img.rfind("&") if img.rfind("&") != None else len(img) - 1
    imgID = img[start : end]

    # Finds the pet ID
    pet = str(info[0])

    # Prints info
    print("imgID:")
    print(imgID)
    print()
    print("ownerID:")
    print(ownerID)
    print()
    print("ownerName:")
    print(ownerName)

print()
