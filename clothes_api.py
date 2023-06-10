import requests

url = "https://asos2.p.rapidapi.com/products/v2/list"

querystring = {"store": "US", "offset": "0", "categoryId": "4209", "limit": "48", "country": "US", "sort": "freshness",
               "currency": "USD", "sizeSchema": "US", "lang": "en-US"}

headers = {
    "X-RapidAPI-Key": "65b2cff2c0msh39a204e48dd0a0dp101f40jsn0b7c20eeb7cf",
    "X-RapidAPI-Host": "asos2.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

# print(response.json()["products"][0:2])
for brands_list in response.json()["products"][0:2]:
    print(brands_list['brandName'])