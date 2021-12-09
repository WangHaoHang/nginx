import socket
import time
if __name__ == '__main__':
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect(('localhost',8087))
        while True:
            str1 = input()
            client.send(bytes(str1,encoding = 'utf-8'))
            str1 = client.recv(1024)
            print(str(str1, encoding='utf-8'))

    except Exception as e:
        print(e)
    finally:
        print('xxx')
        client.shutdown(2)
        client.close()
        print(getattr(client,'_closed'))