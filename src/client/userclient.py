## file: userclient.py is a http request client that sends comment to the redeem server for the user
import httplib,sys
import BeautifulSoup

SERVERPATH = '127.0.0.1'
PORT = 8080

if __name__=='__main__':
    conn = httplib.HTTPConnection(SERVERPATH, PORT)
    
    #register command format: userclient.py register xxxx@xxxx.xx
    #redeem command format  : userclient.py redeem xxxx@xxx.xx 12345678
    
    qrystmt = ''
    try:
        qrystmt = qrystmt + '/' +sys.argv[1]
    except:
        pass
    try:
        qrystmt = qrystmt + '?email=' +sys.argv[2]
    except:
        pass
    try:
        qrystmt = qrystmt + '&redmcode=' +sys.argv[3]
    except:
        pass
    
    print '\nRequest Statment:\n http://%s:%d%s'%(SERVERPATH, PORT, qrystmt)
    conn.request('GET',qrystmt)
    rsp = conn.getresponse()
    soup = BeautifulSoup.BeautifulSoup(rsp.read())
    
    print '\nServer Response:'
    print soup.prettify()
