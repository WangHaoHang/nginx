import socket, time
import threading
from multiprocessing import pool

def transform_info(src_sock: socket.socket, dst_sock: socket.socket):
    flag = True
    try:
        buf = bytes()
        temp = src_sock.recv(1024)
        while temp != None and len(temp) == 1024:
            buf += temp
            temp = src_sock.recv(1024)
        if temp != None:
            buf += temp
        buf = str(buf, encoding='utf-8')
        buf = buf.replace('localhost:8088', 'www.baidu.com')
        buf = bytes(buf, encoding='utf-8')
        dst_sock.send(buf)
        print(buf)
    except Exception as e:
        print('Exception:', e)
        flag = False
    return flag


class NginxObj(object):
    '''
    进行nginx 点对点传输
    '''

    def __init__(self, src_sock: socket.socket, dst_sock: socket.socket):
        self.src_sock = src_sock
        self.dst_sock = dst_sock
        self.flag = True
        self.config = []

    def parse_data(self, data: str):
        pass

    def transform_info(self, data: str):
        pass

    def transform_data(self, src_sock: socket.socket, dst_sock: socket.socket):
        flag = True
        try:
            buf = bytes()
            temp = src_sock.recv(1024)
            while temp != None and len(temp) == 1024:
                buf += temp
                temp = src_sock.recv(1024)
            if temp != None:
                buf += temp
            buf = str(buf, encoding='utf-8')
            buf = buf.replace('localhost:8088', 'www.baidu.com')
            buf = bytes(buf, encoding='utf-8')
            dst_sock.send(buf)
            print(buf)
        except Exception as e:
            print('Exception:', e)
            flag = False
        return flag

    def src2dst(self):
        '''

        :return:
        '''

        while self.flag:
            print('the data from source to the destination')
            self.flag = self.transform_data(self.src_sock, self.dst_sock)
        print('src2dst End !')

    def dst2src(self):
        '''

        :return:
        '''

        while self.flag:
            print('the data from destination to the source')
            self.flag = self.transform_data(self.dst_sock, self.src_sock)
        print('dst2src End !')

    def run(self):
        '''

        :return:
        '''
        print('run')
        t1 = threading.Thread(target=self.src2dst, name='src2dst')
        t1.start()
        t2 = threading.Thread(target=self.dst2src, name='dst2src')
        t2.start()
        while True:
            time.sleep(1)
            print(self.flag, getattr(self.src_sock, "_closed"), getattr(self.dst_sock, "_closed"))
            if self.flag == False:
                break
            # if getattr(self.src_sock,"_closed") == True or getattr(self.dst_sock,"_closed") == True:
            #     print("Yes")
            #     self.flag = False
            #     break
        self.shutdown()

    def shutdown(self):
        try:
            if self.src_sock != None:
                self.src_sock.close()
        except Exception as e:
            print('shutdown src sock!', e)

        try:
            if self.dst_sock != None:
                self.dst_sock.close()
        except Exception as e:
            print('shut down the dst sock!', e)


class NginxManager(object):
    '''
    进行多个nginx_obj管理
    '''

    def __init__(self):
        self.nginx_objs = []

    def add(self, nginx_obj: NginxObj):
        self.nginx_objs.append(nginx_obj)



