from pydantic import BaseModel


class UserCart(BaseModel):
    customer_email: str
    product_name: str
    product_price: str
    product_image_url: str
    count: int
    product_total_price: float
    shop_name: str


class Cart(BaseModel):
    customer_email: str


class RemoveData(BaseModel):
    customer_email: str
    product_name: str


class CountModel(BaseModel):
    customer_email: str
    command: str
    count: int
    product_name: str


class UsersCardData(BaseModel):
    customer_email: str
    card_holder_name: str
    card_number: str
    date: str
    cvv: str


class UsersAddress(BaseModel):
    customer_email: str
    address: str


class UsersInfo(BaseModel):
    email: str
    phone_number: str
    address: str
