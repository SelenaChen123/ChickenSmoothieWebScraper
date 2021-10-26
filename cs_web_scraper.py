# --------------------------------------------------------------------
# CS Web Scraper
# --------------------------------------------------------------------

# Imports libraries
import requests as req
from bs4 import BeautifulSoup as bs
import csv

# Sets base URL and base pet ID
baseURL = "https://www.chickensmoothie.com/viewpet.php?id="
basePetID = 1

# Sets testing constants
normalPetID = 112516469
offAccountPetID = 324851447
deletedPetID = 334526694
staffPetID = 338838141

def printList(list):
    for item in list:
        print(item)


def getList():
    listDatabase = open("list_database.csv", "r")
    reader = csv.reader(listDatabase)
    list = []
    for row in reader:
        if(len(row) == 2):
            list.append(row)

    return {row[0]: row[1] for row in list}


def getPage(id):
    # Gets the page and parses it
    html = req.get(baseURL + str(id)).text
    page = bs(html, "html.parser")

    # Checks to see if pet exists
    exists = page.find("h2") is None

    # Checks to see if pet is off account
    notOffAccount = len(
        page.find("ul", {"class": ["navlinks"]}).select("a")) > 3

    # Returns the page is pet exists and is not off account
    if(exists and notOffAccount):
        return page
    else:
        return None


def getPetInfo(id):
    page = getPage(id)

    if(page is None):
        return None
    else:
        # Finds all pet info
        info = page.find("table", {"class": "spine"}).select(".r")

        # Finds the owner ID and name
        owner = str(info[0].find("a"))
        start = owner.find("u=") + 2
        end = owner.rfind("&") if (
            owner.rfind("&") != None) else len(owner) - 1
        ownerID = owner[start: end]

        start = owner.find(">") + 1
        end = owner.rfind("<")
        ownerName = owner[start: end]

        # Finds the img ID
        img = str(page.find("img", {"id": "petimg"}))
        imgID = ""
        if(img.find("https") != -1):
            start = img.find("?k=") + 3
            end = img.rfind("&") if img.rfind("&") != None else len(img) - 1
            imgID = img[start: end]
        else:
            start = img.find("src=") + 5
            end = img.rfind("\"")
            imgID = "https://www.chickensmoothie.com" + img[start: end]

        # Finds the pet ID
        petID = info[1].text

        # Prints info
        return {"link": baseURL + str(id), "ownerName": ownerName, "ownerID": ownerID, "ID": petID, "imgID": imgID}


def getSpecificPetsWithinRange(img, start, end):
    pets = []
    check = []
    removed = []
    for i in range(end - start + 1):
        try:
            info = getPetInfo(start + i)
            if(info is None):
                removed.append(baseURL + str(start + i))
            elif("https" in info["imgID"]):
                check.append(info["link"])
            elif (info["imgID"] == img):
                pets.append(info["ID"])
        except AttributeError:
            print("error:", baseURL + str(start + i))
    return {"pets": pets, "check": check, "removed": removed}


def main():
    list = getList()

    # results = getSpecificPetsWithinRange(list["Nonballoon"], 45135, 49952)
    results = getSpecificPetsWithinRange(list["Nonballoon"], 45135, 45500)
    print("pets:")
    printList(results["pets"])
    print("\ncheck:")
    printList(results["check"])
    # print("\nremoved:")
    # printList(results["removed"])


print()
main()
print()
