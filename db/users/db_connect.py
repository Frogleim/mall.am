import psycopg2


class Connect:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'mall.am_admin'
        self.user = 'postgres'
        self.password = '0000'

    def connect(self):
        try:
            with psycopg2.connect(host=self.host, database=self.database, user=self.user,
                                  password=self.password) as conn:
                print('Connected Successfully!')
                return conn

        except Exception as e:
            print(f'Error\n{e}')


if __name__ == "__main__":
    my_connect = Connect()
    my_connect.connect()
