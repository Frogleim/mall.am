import json
import firebase_admin
import psycopg2
from firebase_admin import credentials
from firebase_admin import firestore
import random
from .db_connect import Connect


def get_user_information(user_email, phone_number, address=None):
    my_connect = Connect()
    conn = my_connect.connect()

    try:
        with conn.cursor() as cursor:
            insert_query = """INSERT INTO mall_am_clients (email, phone_number, address, 
                            ) VALUES (%s, %s, %s); """

            data = (user_email, phone_number, address)
            cursor.execute(insert_query, data)
            conn.commit()
        print("Saved successfully!")
        return True
    except Exception:
        return False
