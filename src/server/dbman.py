## file: dbm.py is a database manager for access data of redeem server
import sqlite3

class DBmanager:
    def __init__(self, dbpath):
        self.conn = sqlite3.connect(dbpath)
        self.cur = self.conn.cursor()
        
    def createdatabase(self):
        conn = self.conn
        cur = self.cur
        try:
            print '[DBmanager] database creation..',
            cur.execute('''CREATE TABLE EmailRegistration 
                            (redmcode TEXT, email TEXT)''')
            cur.execute('''CREATE TABLE ExchangeRecord
                            (redmcode TEXT, gift TEXT)''')
            conn.commit()
            print 'ok'
            return 1
        
        except:
            print '[DBmanager] database creation fail..'
            return 0
        
    def hasRedmCode(self, code):
        cur = self.cur
        t = (code,)
        results = cur.execute('SELECT * FROM EmailRegistration WHERE redmcode = ?', t)
        if len(results.fetchall()) > 0:
            return True
        else:
            return False
    
    # get redeemed redmcode of the email
    def getEmRedm(self, email):
        cur = self.cur
        t = (email,)
        results = cur.execute('SELECT T1.redmcode, T1.email, T2.gift FROM EmailRegistration T1, ExchangeRecord T2 WHERE T1.redmcode = T2.redmcode AND T1.email=?',t)
        redmlist = []
        for rec in results.fetchall():
            redmlist.append(rec[0])        
        return redmlist
        
    # get registered redeemcode of the email
    def getEmRegi(self, email):
        cur = self.cur
        t = (email,)
        results = cur.execute('SELECT * FROM EmailRegistration WHERE email=?',t)
        redmlist = []
        for rec in results.fetchall():
            redmlist.append(rec[0])
        return redmlist
        
    def saveEmRegi(self, redmcode, email):
        try:
            conn = self.conn
            cur = self.cur
            cur.execute("INSERT INTO EmailRegistration VALUES (?,?)",(redmcode, email,))
            conn.commit()
            return 1
        except:
            print '[DBmanger] data insert process occurs error!!'
            return 0
        
    def saveGtRedm(self, redmcode, gift):
        try:
            conn = self.conn
            cur = self.cur
            cur.execute("INSERT INTO ExchangeRecord VALUES (?,?)",(redmcode, gift))
            conn.commit()
            return 1
        except:
            print '[DBmanger] data insert process occurs error!!'
            return 0
            
    def close(self):
        self.conn.close()
        return 1
    