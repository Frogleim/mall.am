import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random


def auth(service_path):
    if not firebase_admin._apps:
        cred = credentials.Certificate(service_path)
        firebase_admin.initialize_app(cred)


def add_order(customer_email, product_name, product_price, product_image_url, count, service_path):
    auth(service_path)
    db = firestore.client()
    random_doc_id = random.randint(100000, 999999)
    random_id = random.randint(1000, 9999)
    order_data = {
        'order_id': random_id,
        'customer_email': customer_email,
        'product_name': product_name,
        'product_price': product_price,
        'product_image_url': product_image_url,
        'count': count
    }
    try:
        doc_ref = db.collection('users_orders').document(str(random_doc_id))
        doc_ref.set(order_data)
        return True
    except Exception as e:
        print(e)
        return False


def get_data(service_path, field_value):
    orders = []
    auth(service_path=service_path)
    db = firestore.client()
    field_name = 'customer_email'
    query = db.collection('users_orders').where(field_name, '==', field_value)
    results = query.get()
    for doc in results:
        orders.append(doc.to_dict())
    return orders


def remove_data(service_path, field_value):
    auth(service_path=service_path)
    db = firestore.client()
    field_name = 'customer_email'
    try:
        query = db.collection('users_orders').where(field_name, '==', field_value)
        results = query.get()
        for doc in results:
            doc.reference.delete()
            print(f"Document with ID {doc.id} deleted.")
        return True
    except Exception:
        return False


def add_card(customer_email, card_holder_name, card_number, date, cvv, service_path):
    auth(service_path)
    db = firestore.client()
    random_doc_id = random.randint(10, 999999)
    order_data = {
        'customer_email': customer_email,
        'card_holder_name': card_holder_name,
        # 'card_type': card_type,
        'card_number': card_number,
        'date': date,
        'cvv': cvv
    }
    try:
        doc_ref = db.collection('users_card_data').document(str(random_doc_id))
        doc_ref.set(order_data)
        return True
    except Exception as e:
        print(e)
        return False


def add_address(customer_email, address, service_path):
    auth(service_path)
    db = firestore.client()
    random_doc_id = random.randint(10, 999999)
    order_data = {
        'customer_email': customer_email,
        'address': address,

        # 'card_type': card_type,
    }
    try:
        doc_ref = db.collection('users_shipping_address').document(str(random_doc_id))
        doc_ref.set(order_data)
        return True
    except Exception as e:
        print(e)
        return False


def get_address(service_path, customer_email):
    addresses = []
    auth(service_path=service_path)
    db = firestore.client()
    user_email = 'customer_email'
    query = db.collection('users_shipping_address').where(user_email, '==', customer_email)
    result = query.get()
    print(result)
    for docs in result:
        addresses.append(docs.to_dict())
    return addresses


def get_card_information(service_path, field_value):
    orders = []
    auth(service_path=service_path)
    db = firestore.client()
    field_name = 'customer_email'
    query = db.collection('users_card_data').where(field_name, '==', field_value)
    results = query.get()
    for doc in results:
        orders.append(doc.to_dict())
    return orders
