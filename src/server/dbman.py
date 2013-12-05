## file: dbm.py is a database manager for access data of redeem server
import sqlite3

class DBmanager:
    def __init__(self, dbpath):
        self.conn = sqlite3.connect(dbpath)
        self.cur = self.conn.cursor()
        
    def createdatabase(self):
        cur = self.cur
        try:
            cur.execute('''CREATE TABLE EmailRegistration 
                            (redmcode TEXT, email TEXT)''')
            cur.execute('''CREATE TABLE ExchangeRecord
                            (redmcode TEXT, gift TEXT)''')
            cur.commit()
            return 1
        except:
            print '[DBmanager] database creation fail..'
            return 0
            
    