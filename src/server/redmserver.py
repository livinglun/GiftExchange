## file: redmserver is a http server that provide services to register email and redeem gift.

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os,time, urllib, sqlite3
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


class RedmServer:
    def __init__(self):
        self.dbm = dbman.DBmanager(DBPATH)
        # 1. check database is existed
        if not os.path.exists(DBPATH):
            self.dbm.createdatabase()
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
        cmdpath = self.path
        print cmdpath
        if cmdpath.startswith('/register'):
            if '?' not in cmdpath:
                self.wfile.write(ERROR_CMDER)
                return
            query = urllib.splitquery(cmdpath)
            print 'query0', query[0]
            print 'query1', query[1]
            temp = query[1].split('=')
            param = temp[0]
            value = temp[1]
            
            # 1. check email format
            if not util.checkEmail(value):
                self.wfile.write(ERROR_EMFMT)
                return
            # 2. check redeem times
            
            # 3. generate redeem code and check database
            # 4. save email and redeem code
            # 5. return message
            self.wfile.write('<xml><result>succss</result></xml>')
       
        # expected path: /redeem?email=xxx@somewhere&redmcode=xxxxxxxx
        elif self.path.startswith('/redeem'):
            # 1. check redeem code and email is in registration
            # 2. check redeem code is not in redeem record
            # 3. check email redeem times
            # 4. save redeem record into database
            # 5. return message
            self.wfile.write('<xml><result>suceess</result></xml>')
        
        else:
            self.wfile.write(ERROR_NOSRV)
    
if __name__=='__main__':
    svr = RedmServer()