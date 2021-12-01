import socket
import threading
import time
from multiprocessing import pool

def proc_accept(sock:socket.socket):
    while True:
        buf_data = bytes()
        # 获取数据
        temp = sock.recv(1024)
        while temp != None and len(temp) == 1024:
            buf_data = buf_data + temp
            temp = sock.recv(1024)
        if temp != None:
            buf_data += temp
        content = str(buf_data, encoding='utf-8')
        print("Content:", content)
        content = "Server:" + content
        sock.send(bytes(content, encoding='utf-8'))
        if content == 'EOF':
            sock.shutdown(2)
            sock.close()
            break
def create_server(port: int):
    '''
    创建一个简单的服务器，地址为本地地址
    :param port: 端口号
    :return:
    '''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(("localhost", port))
        print('Server:','(localhost,',port,') start!')
        server.listen(3)
        while True:
            # 接受地址
            sock, addr = server.accept()
            print('Server:', '(localhost,', port, ') accept!')
            print("远程连接地址：", addr)
            t1 = threading.Thread(target=proc_accept,args=(sock,),name='xxx')
            t1.start()
    except Exception as e:
        print("Exception:", e)
    finally:
        server.close()


if __name__ == '__main__':
    proc_pool = pool.Pool(10)
    proc_pool.apply_async(func=create_server, args=(8081,))
    proc_pool.apply_async(func=create_server, args=(8082,))
    proc_pool.apply_async(func=create_server, args=(8083,))
    proc_pool.close()
    proc_pool.join()