import json

import firebase_admin
import psycopg2
from firebase_admin import credentials
from firebase_admin import firestore
import random
from .db_connect import Connect


def auth(service_path):
    if not firebase_admin._apps:
        cred = credentials.Certificate(service_path)
        firebase_admin.initialize_app(cred)


def add_to_cart(customer_email, shop_name, product_name, product_price, product_image_url, count, product_total_price):
    my_connect = Connect()
    conn = my_connect.connect()
    try:
        with conn.cursor() as cursor:
            insert_query = """INSERT INTO mall_am_userscart (
            user_email, product_name, shop_name, count, 
            product_image, product_price, product_total_price) VALUES (%s, %s, %s, %s, %s, %s, %s); 
                               """

            data = (customer_email, product_name,  shop_name,  count,  product_image_url, product_price,
                    product_total_price)
            cursor.execute(insert_query, data)
            conn.commit()
        print("Saved successfully!")
        return True
    except Exception as e:
        print(e)
        return False


def get_cart(customer_email):
    my_connect = Connect()
    conn = my_connect.connect()
    try:
        with conn.cursor() as cursor:
            select_query = "SELECT * FROM mall_am_userscart WHERE user_email = %s;"
            cursor.execute(select_query, (customer_email,))
            rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(e)
        return False


def remove_data(customer_email, product_name):
    my_connect = Connect()
    conn = my_connect.connect()
    try:
        with conn.cursor() as cursor:
            delete_query = "DELETE FROM mall_am_userscart WHERE user_email = %s AND product_name = %s;"
            cursor.execute(delete_query, (customer_email, product_name))
            conn.commit()
            print("Rows removed successfully!")
        return True
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return False


def count_handler(customer_email, command, count, product_name):
    my_connect = Connect()
    conn = my_connect.connect()
    try:
        with conn.cursor() as cursor:
            if command == "up":
                count += 1
                change_query = "UPDATE mall_am_userscart SET count = %s WHERE user_email = %s AND product_name = %s"
                cursor.execute(change_query, (count, customer_email, product_name))
                conn.commit()
                print("Rows removed successfully!")
            else:
                count -= 1
                change_query = "UPDATE mall_am_userscart SET count = %s WHERE user_email = %s AND product_name = %s"
                cursor.execute(change_query, (count, customer_email, product_name))
                conn.commit()
                print("Rows removed successfully!")
        return True
    except Exception as error:
        print("Error while connecting to PostgreSQL:", error)
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
    check_address(service_path, customer_email)
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


def check_address(service_path, customer_email):
    addresses = []
    auth(service_path=service_path)
    db = firestore.client()
    user_email = 'customer_email'
    query = db.collection('users_shipping_address').where(user_email, '==', customer_email)
    result = query.get()
    print(result)
    try:
        for docs in result:
            addresses.append(docs.to_dict())
            if len(addresses) != 0:
                print('Address exist, deleting....')
                docs.reference.delete()
    except Exception:
        print(f'No address for user {customer_email}')


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


def insert_credit_card(
        user_email,
        card_number,
        card_date,
        card_cvv,
        card_holder_name
):
    my_connect = Connect()
    conn = my_connect.connect()
    try:
        with conn.cursor() as cursor:
            insert_query = """INSERT INTO mall_am_userspayment (user_email, card_number, card_date, 
                            card_cvv, card_holder_name) VALUES (%s, %s, %s, %s, %s); """

            data = (user_email, card_number, card_date, card_cvv, card_holder_name)
            cursor.execute(insert_query, data)
            conn.commit()
        print("Saved successfully!")
        return True
    except Exception:
        return False


def read_brands():
    my_connect = Connect()
    conn = my_connect.connect()
    try:
        with conn.cursor() as cursor:
            select_query = "SELECT name, logo FROM mall_am_customer;"

            cursor.execute(select_query)
            rows = cursor.fetchall()
            for row in rows:
                name, logo = row
                print(f"Name: {name}, Logo: {logo}")
        print("Saved successfully!")
        return rows
    except Exception:
        return False


def users_information(email, address, phone_number=None):
    my_connect = Connect()
    conn = my_connect.connect()
    try:
        with conn.cursor() as cursor:
            insert_query = "INSERT INTO mall_am_clients (email, phone_number, address) VALUES (%s, %s, %s);"
            data = (email, address, phone_number)
            cursor.execute(insert_query, data)
            conn.commit()
        print("Saved successfully!")

    except Exception:
        pass


def users_orders(email, address, phone_number=None):
    my_connect = Connect()
    conn = my_connect.connect()
    try:
        with conn.cursor() as cursor:
            insert_query = "INSERT INTO mall_am_product (product_price, count, address) VALUES (%s, %s, %s);"
            data = (email, address, phone_number)
            cursor.execute(insert_query, data)
            conn.commit()
        print("Saved successfully!")

    except Exception:
        pass


if __name__ == "__main__":
    read_brands()
