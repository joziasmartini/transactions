import psycopg2
import pandas as pd
import time

try:
    connection = psycopg2.connect(user="postgres",
                                  password="root",
                                  host="127.0.0.1",
                                  database="transactions")
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
    
    start = time.time()
    for x in range(100): # (10002):
        productName = df['Product Name']
        brandName = df['Brand Name']
        asin = df['Asin']

        cursor.execute("insert into Products values (productName, brandName, asin)")
        # cursor.execute("insert into products (product_name, brand_name, asin) values ('nome do produto', 'marca', 'lorem ipsum')")
        connection.commit()
    end = time.time()

    print("Terminooooou")
    print("Tempo gasto:",end - start)


except (Exception, psycopg2.DatabaseError) as error:
    print("Deu caca\n")
    print(error)
    connection.rollback()

finally:
    # Fecha a conexão com o banco de dados
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
