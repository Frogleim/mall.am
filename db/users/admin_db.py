import psycopg2
from datetime import datetime
import pytz


def insert_data(data):
    current_utc_datetime = datetime.utcnow()
    local_timezone = pytz.timezone('Asia/Yerevan')
    current_datetime = current_utc_datetime.astimezone(local_timezone)
    print(current_datetime)

    try:
        # Connect to the PostgreSQL database using 'with' statement
        with psycopg2.connect(
                host="localhost",
                database="mall.am_admin",
                user="postgres",
                password="0000"
        ) as conn:
            # Create a cursor to interact with the database
            with conn.cursor() as cursor:
                # Define the SQL query to insert data
                insert_query = """INSERT INTO mall_am_product (product_price, count, product_image_url, 
                customer_email, product_name, order_id, order_time) VALUES (%s, %s, %s, %s, %s, %s, %s); """

                # Data to be inserted
                for items in data:
                    price_str = items['product_price'].replace("$", "").replace(",", "")
                    price_str = price_str[:-3]
                    data = (int(price_str), items['count'], items['product_image_url'], items['customer_email'],
                            items['product_name'], items['order_id'], current_datetime)

                    # Execute the query with the data
                    cursor.execute(insert_query, data)

                    # Commit the changes to the database (not required for all queries)
                    conn.commit()

        print("Data inserted successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or inserting data:", error)

# Usage example:
