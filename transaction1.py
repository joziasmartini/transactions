import psycopg2
import pandas as pd
import asyncio

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
        await asyncio.gather(self.executeExplicit())
        await asyncio.gather(self.executeImplicit())

    async def executeExplicit(self):
        print('hello')

    async def executeImplicit(self):
        print('hello 1')

    async def showRows(self):
        pass

bd = Banco()
bd.connect()
asyncio.run(bd.runTransaction())