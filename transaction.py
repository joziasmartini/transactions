import psycopg2
import pandas as pd
import asyncio
import timeit

class Database:
    def connect(self):
        try:
            self.connection = psycopg2.connect(user="postgres", password="root", host="127.0.0.1", database="transactions")
            self.connection.autocommit = False
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print("We got an error.\n")
            print(error)

    async def runTransaction(self):
        #inicio = timeit.default_timer()
        #await asyncio.gather(self.executeExplicit())
        #fim = timeit.default_timer()
        #print ('duracao explicita = : %f' % (fim - inicio))
        inicio = timeit.default_timer()
        await asyncio.gather(self.executeImplicit())
        fim = timeit.default_timer()
        print ('Time duration: %f' % (fim - inicio))
        self.connection.close()
        self.cursor.close()

    async def executeExplicit(self):
        try:
            query = "BEGIN"
            self.cursor.execute(query)

            self.df = pd.read_csv('data.csv')
            for x in range(10002):
                ab = (x + 20) * 2 + 5
                self.cursor.execute("""INSERT INTO product VALUES (%s, %s);""",(ab, self.df['Product Name'] [x]))

        except(Exception, psycopg2.DatabaseError) as error:
            print("We got an error.\n")
            print(error)
            self.connection.rollback()
            return 1

        finally:
            self.connection.commit()
            return 0  

    async def executeImplicit(self):
        self.df = pd.read_csv('data.csv')
        for x in range(10002):
            ab = (x + 20) * 2 + 5
            try:
                self.cursor.execute("""INSERT INTO product VALUES (%s, %s);""",(ab, self.df['Product Name'] [x]))
        
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: Line "+ str(x) +" can not be inserted.\n")
                print(error)

databaseInstance = Database()
databaseInstance.connect()
asyncio.run(databaseInstance.runTransaction())