import mysql.connector

db='library_with_sql'
host='localhost'
password='rootPassword1919'
user='root'

def my_connect():
    try:
        conn = mysql.connector.connect(
            database=db,
            host=host,
            password=password,
            user=user
            )
        print('MYSQL is now connect')
        return conn   
    except Exception as e:
        print(f'Error:{e}')
        return None
