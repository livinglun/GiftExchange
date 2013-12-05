## file: redmserver is a http server that provide services to register email and redeem gift.

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os,time, urllib, sqlite3, random
import dbman, util

DBPATH = 'redmdb.db'
SERVERPATH = '127.0.0.1'
SERVERPORT = 8080

ERROR_CMDER = '<xml><error>command format error</error></xml>' # command error
ERROR_EMFMT = '<xml><error>email format error</error></xml>' # email format error
ERROR_EMLMT = '<xml><error>email redeem limitation is 3</error></xml>' # email redeem limitation
ERROR_NOREG = '<xml><error>no such redeem code</error></xml>' # no such email and redeem code registration
ERROR_RCUSE = '<xml><error>the redeem code has been used</error></xml>' # the redeem code has been used
ERROR_NOSRV = '<xml><error>there provide no such service</error></xml>' # there is no such service

GIFTLIST = ['gift01','gift02','gift03','gift04','gift05','gift06','gift07','gift08','gift09','gift10']

class RedmServer:
    def __init__(self):
        
        # 1. check database is existed
        print '[RedmServer]database checking..',
        if not os.path.exists(DBPATH):
            print 'no database'
            self.dbm = dbman.DBmanager(DBPATH)
            self.dbm.createdatabase()
            self.dbm.close()
        else:
            print 'ok'
            
        # 2. set parameter and start up the server
        server = HTTPServer
        httpd = server(('localhost',8080), RedmHandler)
        print time.asctime(), "Server Starts - %s:%s" % (SERVERPATH, SERVERPORT)
        httpd.serve_forever()
        
class RedmHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # database perpetration
        dbm = dbman.DBmanager(DBPATH)
        
        # response setting
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        # expected path: /register?email=xxx@somewhere
        query = urllib.splitquery(self.path)
        
        if len(query) < 2:
            self.wfile.write(ERROR_CMDER)
            return
            
        service = query[0]
        qrystmt = query[1] # query statement
        #print '[RedmHandler]service:', service
        #print '[RedmHandler]query:', qrystmt
            
        if service == '/register':
            try:
                temp = qrystmt.split('=')
                param = temp[0]
                value = temp[1]
            except:
                self.wfile.write(ERROR_CMDER)
                return
            
            # 1. check email format
            if param != 'email':
                self.wfile.write(ERROR_CMDER)
                return
                
            if not util.checkEmail(value):
                self.wfile.write(ERROR_EMFMT)
                return
                
            # 2. check redeem times
            redmtime = len(dbm.getEmRedm(value))
            if redmtime >= 3:
                self.wfile.write(ERROR_EMLMT)
                return
                
            # 3. generate redeem code and check database
            redmcode = None
            loop = True
            while loop:
                redmcode = self.genRedmCode()
                if not dbm.hasRedmCode(redmcode):
                    loop = False
                    
            # 4. save email and redeem code
            dbm.saveEmRegi(redmcode, value)
            
            # 5. return message
            rpstmt = '<xml><result>email registration succss</result>\
            <email>%s</email>\
            <redmcode>%s</redmcode></xml>'%(value, redmcode)
            self.wfile.write(rpstmt)
       
        # expected path: /redeem?email=xxx@somewhere&redmcode=xxxxxxxx
        elif service == '/redeem':
            try:
                temp = qrystmt.split('&')
                emailstmts = temp[0].split('=')
                codestmts = temp[1].split('=')
                emailpara = emailstmts[0]
                emailvalue = emailstmts[1]
                codepara = codestmts[0]
                codevalue = codestmts[1]
            except:
                self.wfile.write(ERROR_CMDER)
                return
            
            if (emailpara != 'email') or (codepara != 'redmcode'):
                self.wfile.write(ERROR_CMDER)
                return
            
            # 1. check redeem code and email is in registration
            regicodes = dbm.getEmRegi(emailvalue)
            if codevalue not in regicodes:
                self.wfile.write(ERROR_NOREG)
                return
                
            # 2. check redeem code is not in redeem record
            redmrecords = dbm.getEmRedm(emailvalue)
            if codevalue in redmrecords:
                self.wfile.write(ERROR_RCUSE)
                return 
                
            # 3. check email redeem times
            redmtime = len(dbm.getEmRedm(emailvalue))
            if redmtime >= 3:
                self.wfile.write(ERROR_EMLMT)
                return
            
            # 4. get gift and save redeem record into database
            gift = self.getGift(codevalue)
            dbm.saveGtRedm(codevalue, gift)
            
            # 5. return message
            rpstmt = '<xml><result>gift redeem succss</result>\
            <email>%s</email>\
            <redmcode>%s</redmcode>\
            <gift>%s</gift></xml>'%(emailvalue, codevalue, gift)
            self.wfile.write(rpstmt)
        
        else:
            self.wfile.write(ERROR_NOSRV)
            
    def genRedmCode(self):
        ## ascii 'a' = 97, 'z' = 122
        codespace = []
        redmcode = ''
        for num in range(10):
            codespace.append(str(num))
        for asc in range(97,123):
            codespace.append(str(unichr(asc)))
        for idx in range(8):
            redmcode = redmcode+(random.choice(codespace))
        return redmcode
        
    def getGift(self, code):
        codesum = 0
        for cha in code:
            codesum = codesum + ord(cha)
        select = codesum%len(GIFTLIST)
        return GIFTLIST[select]
    
if __name__=='__main__':
    svr = RedmServer()