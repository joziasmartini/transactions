import psycopg2
import pandas as pd
import asyncio
import time
import timeit

class Banco:
    def connect(self):
        try:
            self.connection = psycopg2.connect(user="postgres", password="root", host="127.0.0.1", database="transactions")
            self.connection.autocommit = False
            self.cursor = self.connection.cursor()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print("Deu caca\n")
            print(error)

    async def runTransaction(self):
        inicio = timeit.default_timer()
        await asyncio.gather(self.executeExplicit())
        fim = timeit.default_timer()
        print ('duracao explicita = : %f' % (fim - inicio))
        #inicio = timeit.default_timer()
        #await asyncio.gather(self.executeImplicit())
        #fim = timeit.default_timer()
        #print ('duracao implicita = : %f' % (fim - inicio))

    async def executeExplicit(self):
        try:
            query = "BEGIN"
            self.cursor.execute(query)

            self.df = pd.read_csv('data.csv')
            for x in range(10002): # (10002):
                #print(self.df['Product Name'] [x])
                ab = x + 10
                query = "insert into product values( " + str(ab) + ", " + self.df['Product Name'] [x] + ")"
                # print(query)
                self.cursor.execute(query)

        except(Exception, psycopg2.DatabaseError) as error:
            print("Deu caca\n")
            print(error)
            self.connection.rollback()
            return 1

        finally:
            self.connection.commit()
            return 0  

    async def executeImplicit(self):
        try:
            self.df = pd.read_csv('data.csv')
            for x in range(10002): # (10002):
                #print(self.df['Product Name'] [x])
                ab = x + 10
                query = "insert into product values( " + str(ab) + ", " + self.df['Product Name'] [x] + ")"
                print(query)
                #cursor.execute(query)
        
        except (Exception, psycopg2.DatabaseError) as error:
            print("Deu caca\n")
            print(error)
            self.connection.rollback()

banco = Banco()
banco.connect()
# Banco.connect(self)
asyncio.run(banco.runTransaction())
# Banco.executeExplicit()
# Banco.executeImplicit()
# Banco.executeExplicitWithRollback()
# Banco.executeImplicitWithRollback()
