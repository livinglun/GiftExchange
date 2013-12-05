import httplib

conn = httplib.HTTPConnection('localhost', 8080)
conn.request('GET','/register?email=@living@gmail.com')
rsp = conn.getresponse()

print rsp.status, rsp.reason
print rsp.read()
