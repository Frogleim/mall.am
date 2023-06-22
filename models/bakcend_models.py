from pydantic import BaseModel


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


class UsersCardData(BaseModel):
    customer_email: str
    card_holder_name: str
    card_number: str
    date: str
    cvv: str


class UsersAddress(BaseModel):
    customer_email: str
    address: str

