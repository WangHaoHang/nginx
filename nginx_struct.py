import socket, time
import threading
from multiprocessing import pool
from request_header import header


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
        self.head_info = header()
        self.xdata = ''

    def parse_data(self, data: str):
        dats = data.split('\n')
        self.head_info.add_url(dats[0])
        flag = 0
        self.xdata = ''
        for dat in dats[1:]:
            if flag == 0:
                if dat.strip() == '':
                    flag = 1
                else:
                    self.head_info.add_info(dat)
            else:
                self.xdata += dat + '\n'
        print('head_info-start')
        print(self.head_info.string())
        print('head_info-end')

    def transform_info(self, data: str):
        pass

    def send_str(self, sock: socket.socket, data: str):
        flag = True
        try:
            buf = bytes(data, encoding='utf-8')
            sock.send(buf)
        except Exception as e:
            print('send str exception', e)
            flag = False
        return flag

    def recv_str(self, sock: socket.socket):
        flag = True
        # sock.settimeout(10)
        buf = bytes()
        try:
            temp = sock.recv(1024)
            while temp is not None and len(temp) == 1024:
                buf += temp
                temp = sock.recv(1024)
            if temp is not None and len(temp) > 0:
                buf += temp
        except Exception as e:
            print('recv str exception:', e)
            flag = False
        finally:
            buf = str(buf, encoding='utf-8')
            if buf.strip() == '':
                flag = False
        return buf, flag

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
            print(buf)
            buf = buf.replace('localhost:8088', 'www.baidu.com')
            buf = bytes(buf, encoding='utf-8')
            dst_sock.send(buf)
            print(str(buf,encoding='utf-8'))
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
            # self.transform_data(self.src_sock,self.dst_sock)

            buf, self.flag = self.recv_str(self.src_sock)
            if self.flag == False:
                break
            print('orgin_buf:')
            print(buf)
            self.head_info.clear()
            self.xdata = ''
            self.parse_data(buf)
            self.head_info.all_info['Host'] = 'www.baidu.com'
            # self.head_info.all_info['Cookie'] = None
            buf = ''
            for x in self.head_info.request_url:
                buf += x.strip() +' '
            buf = buf.strip()
            buf += '\n'
            buf += self.head_info.string()
            buf += self.xdata
            print('buf:')
            print(buf)
            self.flag = self.send_str(self.dst_sock, data=buf)
        print('src2dst End !')

    def dst2src(self):
        '''

        :return:
        '''

        while self.flag:
            print('the data from destination to the source')
            buf, self.flag = self.recv_str(self.dst_sock)
            if self.flag == False:
                break
            print(buf,self.flag)
            self.flag = self.send_str(self.src_sock, data=buf)
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
