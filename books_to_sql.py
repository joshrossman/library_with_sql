from connect_sql import my_connect

def book_to_database(title,author_name,isbn,publication_date,availability):
    
    conn=my_connect()
    cursor=conn.cursor()
    try:
        query='SELECT id FROM authors WHERE name LIKE %s'
        cursor.execute(query,(author_name,))
        author_id=cursor.fetchall()[0][0]
        print(author_id)
        if author_id:
            query='''INSERT INTO books(title,author_id,isbn,publication_date,availability) 
            VALUES (%s,%s,%s,%s,%s);
            '''
            
            cursor.execute(query,(title,author_id,isbn,publication_date,availability))
            conn.commit()
            print('Book Added.')
        else:
            print("Error: Not a valid author. Please first add author to the database.")        
    except Exception as e:
        print(f'Error:{e}')
    finally:
        if conn and conn.is_connected():
            conn.close()
            cursor.close()
