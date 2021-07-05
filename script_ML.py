# PACKAGES

import requests
import json


# MAIN PROGRAM

# define seller ID and site ID

sellerID = 179571326
siteID = "MLA"

# Generate LOG File

file = open(f"seller_{str(sellerID)}_{siteID}.txt", "wt")

file.write(f"Seller ID: {sellerID}\n")
file.write(f"Site ID: {siteID}\n")

# Stablish a connection with the API

try:
    productsAPIRequest = requests.get("https://api.mercadolibre.com/sites/" + siteID + "/search?seller_id=" + str(sellerID))
except:
    file.write("\nERROR: Couldn't stablish a connection with the seller's information API.\n")
else:
    file.write("\nINFO: Connection with seller's information API succesfully reached.\n")
    products = json.loads(productsAPIRequest.content)

    # Cargar datos en el archivo de LOG

    largestID = 0
    largestTitle = 0
    largestCatID = 0
    largestCatName = 0
    table = []
    categories = dict()

    for p in products["results"]:
        currentID = p["id"]
        currentTitle = p["title"]
        currentCatID = p["category_id"]
        try:
            if currentCatID not in categories.keys():
                currentCatAPI = requests.get("https://api.mercadolibre.com/categories/" + p["category_id"])
                currentCategory = json.loads(currentCatAPI.content)
                categories[currentCatID] = currentCategory["name"]
        except:
            categories[currentCatID] = "###"
            currentCatName = "###"
        else:
            currentCatName = categories[currentCatID]
        table.append((p["id"], p["title"], p["category_id"], currentCatName))
        lengthID = len(currentID)
        lengthTitle = len(currentTitle)
        lengthCatID = len(currentCatID)
        lengthCatName = len(currentCatName)
        if lengthID > largestID:
            largestID = lengthID
        if lengthTitle > largestTitle:
            largestTitle = lengthTitle
        if lengthCatID > largestCatID:
            largestCatID = lengthCatID
        if lengthCatName > largestCatName:
            largestCatName = lengthCatName

    file.write("\nProduct ID".center(largestID + 5) + "Title".center(largestTitle + 5)
               + "Category ID".center(largestCatID + 5) + "Name".center(largestCatName + 5) + "\n")
    file.write("-" * (largestID + largestTitle + largestCatID + largestCatName + 20) + "\n")

    for row in table:
        file.write(row[0].center(largestID + 5) + row[1].center(largestTitle + 5) +
                   row[2].center(largestCatID + 5) + row[3].center(largestCatName + 5) + "\n")

    file.write("\nINFO: All data gathered can be seen in the previous table.\n")
    file.write("\n###: It indicates that some category name couldn't be found.\n")