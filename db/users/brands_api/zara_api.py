import requests


def get_products(category_id):

    print(category_id)
    products_list = []
    url = f"https://www.zara.com/am/en/category/{category_id}/products?ajax=true"
    print(url)

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Referer": "https://www.zara.com/am/ru/zhenshchiny-kurtki-l1114.html?v1=2290770",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    response = requests.get(url, headers=headers)
    data = response.json()['productGroups']
    for items in data[0]['elements']:
        try:
            image_path = items['commercialComponents'][0]['xmedia'][0]['path']
            name = items['commercialComponents'][0]['xmedia'][0]['name']
            timestamp = items['commercialComponents'][0]['xmedia'][0]['timestamp']
            image_url = f'https://static.zara.net/photos//{image_path}/w/613/{name}.jpg?ts={timestamp}'
            product_name = items['commercialComponents'][0]['name']
            price = items['commercialComponents'][0]['price']
            product_id = items['commercialComponents'][0]['id']
            converted_price = price / 100
            formatted_price = "{:.2f}".format(converted_price)
            products_dict = {
                "product_id": product_id,
                "name": product_name,
                "price": formatted_price,
                "image": image_url
            }
            products_list.append(products_dict)
        except Exception:
            print('Not found')
    print(products_list)
    return products_list


def get_categories():
    categories_list = []
    url = "https://www.zara.com/am/en/categories?categoryId=2290770&categorySeoId=1114&ajax=true"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36",

        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Referer": "https://www.zara.com/am/ru/%D0%BA%D0%BE%D0%BC%D0%B1%D0%B8%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0"
                   "%BD%D0%BD%D0%B0%D1%8F-%D0%B4%D0%B6%D0%B8%D0%BD%D1%81%D0%BE%D0%B2%D0%B0%D1%8F-%D0%BA%D1%83%D1%80"
                   "%D1%82%D0%BA%D0%B0-%D0%B1%D0%BE%D0%BC%D0%B1%D0%B5%D1%80-zw-p02553242.html?v1=276030645&v2=2290770",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response = requests.get(url, headers=headers)
    categories = response.json()['categories'][0]['subcategories']
    grid_items = [item for item in categories if item['contentType'] == 'grid']
    for items in grid_items:
        try:
            capitalized_string = items['name'].capitalize()
            categories_dict = {
                "category_id": items['id'],
                "category_name": capitalized_string
            }
            print('Ok')
            categories_list.append(categories_dict)
        except Exception:
            print('None')
    return categories_list
