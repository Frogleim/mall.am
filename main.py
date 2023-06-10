from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from starlette.middleware.cors import CORSMiddleware
from db.users import users_orders


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


class UserOrder(BaseModel):
    customer_email: str
    product_name: str
    product_price: str
    product_image_url: str
    count: str


class Cart(BaseModel):
    customer_email: str


class RemoveData(BaseModel):
    customer_email: str


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
def make_order(body: UserOrder):
    service_path = './db/users/services/ontime-bca87-firebase-adminsdk-hpaht-6e95f71370.json'
    order = users_orders.add_order(
        body.customer_email,
        body.product_name,
        body.product_price,
        body.product_image_url,
        body.count,
        service_path

    )
    if order:
        return {"Message": "Success"}
    else:
        raise HTTPException(status_code=400, detail="Something Went wrong! Please try again")


@app.get('/cart/{customer_email}')
def get_order(customer_email: str):
    service_path = './db/users/services/ontime-bca87-firebase-adminsdk-hpaht-6e95f71370.json'
    orders = users_orders.get_data(service_path=service_path, field_value=customer_email)
    return orders


@app.get('/check_cart/{customer_email}')
def check_order(customer_email: str):
    service_path = './db/users/services/ontime-bca87-firebase-adminsdk-hpaht-6e95f71370.json'
    orders = users_orders.get_data(service_path=service_path, field_value=customer_email)
    print(type(orders))
    if len(orders) == 0:
        return "null"
    else:
        return 0


@app.post('/remove_data')
def remove_data(body: RemoveData):
    service_path = './db/users/services/ontime-bca87-firebase-adminsdk-hpaht-6e95f71370.json'
    remove_data_in_cart = users_orders.remove_data(service_path=service_path, field_value=body.customer_email)
    if remove_data_in_cart:
        return {"Message": "Success"}
    else:
        return {"Message": "false"}


@app.get('/clothes')
def clothes():
    print(get_clothes())
    return get_clothes()
