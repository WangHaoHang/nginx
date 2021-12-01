import socket,os
import http.client
if __name__ == '__main__':
    # req = urllib.request.urlopen("http://www.baidu.com")
    # print(req.getheaders())
    # print(req.read())

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    addr = socket.gethostbyname("www.baidu.com")
    try:
        client.connect(('www.baidu.com',80))
        fd = open('1.txt','r')
        lines = fd.readlines()
        request = ""
        for line in lines:
            request += line
        print(addr)
        print(request)
        flag = client.send(bytes(request,encoding='utf-8'))
        buf = ""
        temp = client.recv(1024)
        print(str(temp,encoding='utf-8'))
        while len(temp) == 1024:
            buf += str(temp,encoding='utf-8')
            temp = client.recv(1024)
        print(buf+str(temp,encoding='utf-8'))
    except Exception as e:
        print('E',e)
    finally:
        client.close()