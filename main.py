import json
from fastapi import FastAPI, HTTPException
import requests
from starlette.middleware.cors import CORSMiddleware
from db.users import users_orders
from models import bakcend_models
from collections import defaultdict


def get_clothes():
    url = "https://asos2.p.rapidapi.com/products/v2/list"

    querystring = {"store": "US", "offset": "0", "categoryId": "4209", "limit": "48", "country": "US",
                   "sort": "freshness",
                   "currency": "USD", "sizeSchema": "US", "lang": "en-US"}

    headers = {
        "X-RapidAPI-Key": "65b2cff2c0msh39a204e48dd0a0dp101f40jsn0b7c20eeb7cf",
        "X-RapidAPI-Host": "asos2.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/add_to_cart')
def add_to_cart(body: bakcend_models.UserCart):
    user_cart = users_orders.add_to_cart(
        body.customer_email,
        body.shop_name,
        body.product_name,
        body.product_price,
        body.product_image_url,
        body.count,
        body.product_total_price,
    )
    if user_cart:
        return {"Message": "Success"}
    else:
        raise HTTPException(status_code=400, detail="Something Went wrong! Please try again")


@app.get('/cart/{customer_email}')
def get_cart(customer_email: str):
    data = users_orders.get_cart(customer_email)

    return {"Message": data}


@app.get('/check_cart/{customer_email}')
def check_order(customer_email: str):
    orders = users_orders.get_cart(customer_email)
    print(type(orders))
    if len(orders) == 0:
        return "null"
    else:
        return 0


@app.post('/remove_data')
def remove_data(body: bakcend_models.RemoveData):
    remove_data_in_cart = users_orders.remove_data(body.customer_email, body.product_name)
    if remove_data_in_cart:
        return {"Message": "Success"}
    else:
        return {"Message": "false"}


@app.post('/change_count')
def change_count(body: bakcend_models.CountModel):
    count_model_handler = users_orders.count_handler(
        body.customer_email,
        body.command,
        body.count,
        body.product_name
    )
    if count_model_handler:
        return {'Message': "Count Changed Successfully"}
    else:
        raise HTTPException(status_code=400, detail="Something Went wrong! Please try again")


@app.post('/add_card/')
def add_card(body: bakcend_models.UsersCardData):
    service_path = './db/users/services/ontime-bca87-firebase-adminsdk-hpaht-6e95f71370.json'
    add_card_information = users_orders.add_card(
        body.customer_email,
        body.card_holder_name,
        body.card_number,
        body.date,
        body.cvv,
        service_path
    )

    if add_card_information:
        return {"Message": "Success"}
    else:
        return {"Message": 'false'}


@app.post('/add_address/')
def add_delivery_address(body: bakcend_models.UsersAddress):
    service_path = './db/users/services/ontime-bca87-firebase-adminsdk-hpaht-6e95f71370.json'
    add_address = users_orders.add_address(
        body.customer_email,
        body.address,
        service_path
    )
    if add_address:
        return {"Message": 'Success'}
    else:
        return {'Message': "False"}


@app.get('/address/{customer_email}')
def get_users_address(customer_email: str):
    service_path = './db/users/services/ontime-bca87-firebase-adminsdk-hpaht-6e95f71370.json'
    address = users_orders.get_address(service_path=service_path, customer_email=customer_email)
    for docs in address:
        print(docs['address'])
        street_address = docs['address'].split(', ')[0]
        city = docs['address'].split(', ')[1]
        zipcode = docs['address'].split(', ')[2]
        country = docs['address'].split(', ')[3]
        return {
            "customer_email": docs['customer_email'],
            "street": street_address,
            "city": city,
            "zipcode": zipcode,
            "country": country
        }


@app.get('/clothes')
def clothes():
    print(get_clothes())
    return get_clothes()


@app.get('/get_card_information/{customer_email}')
def get_card_information(customer_email: str):
    service_path = './db/users/services/ontime-bca87-firebase-adminsdk-hpaht-6e95f71370.json'
    orders = users_orders.get_card_information(service_path=service_path, field_value=customer_email)
    print(type(orders))
    return orders


@app.get('/check_card_information/{customer_email}')
def check_card_information(customer_email: str):
    service_path = './db/users/services/ontime-bca87-firebase-adminsdk-hpaht-6e95f71370.json'
    orders = users_orders.get_card_information(service_path=service_path, field_value=customer_email)
    print(type(orders))
    if len(orders) > 0:
        return 0
    else:
        raise HTTPException(status_code=404, detail=f'No card information for user {customer_email}')


@app.get('/brands/')
def get_brands():
    brands_data = users_orders.read_brands()
    print(brands_data)
    brands_list = []
    for rows in brands_data:
        name, logo = rows
        d = {
            "name": name,
            "logo": logo
        }
        print(d)
        brands_list.append(d)
    return brands_list


@app.get('/check_shop/{shop_name}')
def check_shop(shop_name: str):
    if shop_name == 'asos':
        return {"Message": "found", "type": "asos"}
    elif shop_name == 'mall':
        return {"Message": "found", "type": "mall"}
    else:
        raise HTTPException(status_code=404, detail='Not found')
