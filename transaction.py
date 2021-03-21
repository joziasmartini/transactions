import psycopg2
import pandas as pd

try:
    connection = psycopg2.connect(user="postgres",
                                  password="root",
                                  host="127.0.0.1",
                                  database="postgres")
    connection.autocommit = False
    cursor = connection.cursor()

    query = "drop table if exists Products"
    cursor.execute(query)
    connection.commit()

    query = """create table if not exists Products(
        product_name varchar(100),
        brand_name varchar(100),
        asin varchar(100)
    )"""
    cursor.execute(query)
    connection.commit()

    print("Chegou aq")

    #Começa inserção banco

    df = pd.read_csv('data.csv')

    for x in range(10002):
        print(df['Product Name'] [x], end='')
        print(' ')
        print(df['Brand Name'] [x], end='')
        print(' ')
        print(df['Asin'] [x], end='')

except (Exception, psycopg2.DatabaseError) as error:
    print("Deu caca\n")
    print(error)
    connection.rollback()

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
