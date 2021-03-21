import psycopg2

try:
    connection = psycopg2.connect(user="postgres",
                                  password="root",
                                  host="127.0.0.1",
                                  database="transactions")
    connection.autocommit = True
    cursor = connection.cursor()
    amount = 2500

    query = "drop database if exists transactions"
    cursor.execute(query)


    query = "create database transactions"
    cursor.execute(query)


    query = """create table if not exists produtos(
        product_name varchar(100),
        brand_name varchar(100),
        asin varchar(100)
    )"""
    
    cursor.execute(query)
    
    connection.commit()
    print("Transaction completed successfully ")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error in transction Reverting all other operations of a transction ", error)
    connection.rollback()

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
