import random
import socket, time
import threading
from multiprocessing import pool
from request_header import header
from config import Config


def transform_info(src_sock: socket.socket, dst_sock: socket.socket):
    flag = True
    try:
        buf = bytes()
        temp = src_sock.recv(1024)
        while temp is not None and len(temp) == 1024:
            buf += temp
            temp = src_sock.recv(1024)
        if temp is not None:
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

    def __init__(self, src_sock: socket.socket, dst_sock: socket.socket, config: Config):
        self.src_sock = src_sock
        self.dst_sock = dst_sock
        self.flag = True
        self.config = config
        self.head_info = header()
        self.xdata = ''
        self.orgin_context = ''

    def parse_data(self, data: str):
        '''
        解析 报文
        :param data:
        :return:
        '''
        # url
        dats = data.split('\n')
        self.head_info.add_url(dats[0])
        flag = 0

        self.xdata = ''
        for dat in dats[1:]:
            if flag == 0:
                if dat.strip() == '':
                    flag = 1
                else:
                    # head
                    self.head_info.add_info(dat)
            else:
                # body
                self.xdata += dat + '\n'
        print('head_info-start')
        print(self.head_info.string())
        print('head_info-end')

    def get_send_info(self):
        '''

        :return:
        '''
        # request url
        buf = ''
        for x in self.head_info.request_url:
            buf += x.strip() + ' '
        buf = buf.strip()
        buf += '\n'
        # request head
        buf += self.head_info.string()
        # request data
        buf += self.xdata
        return buf

    def set_head_info(self):
        '''

        :return:
        '''
        # 修改 Host
        remote_addr = str(self.config.remote_addr[0][0])
        if remote_addr.startswith('http'):
            self.head_info.all_info['Host'] = remote_addr.replace('http://', '')
        else:
            self.head_info.all_info['Host'] = remote_addr

        # 修改 request_url
        now_url = self.head_info.request_url[1]
        now_url = str(now_url)
        local_url = self.config.local_url
        remote_url = self.config.remote_url[0]
        print('url:',local_url,remote_url)
        if now_url.find(local_url) >= 0:
            if local_url == '/':
                if str(remote_url).endswith('/'):
                    self.head_info.request_url[1] = remote_url[0:-1] + now_url
                else:
                    self.head_info.request_url[1] = remote_url + now_url[1:]
            else:
                self.head_info.request_url[1] = now_url.replace(local_url, remote_url)
        print('request_url:',self.head_info.request_url[1])
    def send_str(self, sock: socket.socket, data: str):
        '''

        :param sock:
        :param data:
        :return:
        '''
        flag = True
        try:
            buf = bytes(data, encoding='utf-8')
            sock.send(buf)
        except Exception as e:
            print('send str exception', e)
            flag = False
        return flag

    def recv_str(self, sock: socket.socket):
        '''

        :param sock:
        :return:
        '''
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
        '''

        :param src_sock:
        :param dst_sock:
        :return:
        '''
        flag = True
        try:
            buf = bytes()
            temp = src_sock.recv(1024)
            while temp is not None and len(temp) == 1024:
                buf += temp
                temp = src_sock.recv(1024)
            if temp is not None:
                buf += temp
            buf = str(buf, encoding='utf-8')
            print(buf)
            buf = buf.replace('localhost:8088', 'www.baidu.com')
            buf = bytes(buf, encoding='utf-8')
            dst_sock.send(buf)
            print(str(buf, encoding='utf-8'))
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
            # 之前成功的方法
            # self.transform_data(self.src_sock,self.dst_sock)

            buf, self.flag = self.recv_str(self.src_sock)
            if not self.flag:
                break
            self.orgin_context = buf

            print('origin_context:')
            print(self.orgin_context)

            # 清空 解析数据
            self.head_info.clear()
            self.xdata = ''

            # 数据解析
            self.parse_data(buf)

            # 数据头部转换
            self.set_head_info()
            # self.head_info.all_info['Host'] = 'www.baidu.com'

            # 生成新的报文
            buf = self.get_send_info()
            print('modify_context:')
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
            if not self.flag:
                break
            print(buf, self.flag)
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
            time.sleep(60)
            print(self.flag, getattr(self.src_sock, "_closed"), getattr(self.dst_sock, "_closed"))
            if self.flag == False:
                break
            # if getattr(self.src_sock,"_closed") == True or getattr(self.dst_sock,"_closed") == True:
            #     print("Yes")
            #     self.flag = False
            #     break
        self.shutdown()

    def shutdown(self):
        '''
        关闭socket 输入和输出
        :return:
        '''
        try:
            if self.src_sock is not None:
                self.src_sock.close()
        except Exception as e:
            print('shutdown src sock!', e)

        try:
            if self.dst_sock is not None:
                self.dst_sock.close()
        except Exception as e:
            print('shut down the dst sock!', e)


class NginxManager(object):
    '''
    进行多个nginx_obj管理
    '''

    def __init__(self):
        self.nginx_objs = []
        self.config = None
        self.server = None
        self.name = ''

    def set_name(self, name: str):
        self.name = name

    def add(self, nginx_obj: NginxObj):
        self.nginx_objs.append(nginx_obj)

    def add_config(self, config):
        self.config = config

    def build_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(('localhost', self.config.local_port))
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.listen(5)
        except Exception as e:
            print("create Server is Error!")
            print("the exception is ", e)

    def remove_nginx(self):
        pass

    def run(self):
        self.build_server()
        while True:
            src_socket, addr = self.server.accept()
            print('accept:',addr)
            dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            '''
                先写一个随机选择算法
            '''
            size = len(self.config.remote_addr)
            index = random.randint(0,size-1)
            print('index:',index)
            dst_socket.connect((self.config.remote_addr[index][0], int(self.config.remote_addr[index][1])))
            nginx_obj = NginxObj(src_socket, dst_socket, config=self.config)
            self.nginx_objs.append(nginx_obj)
            t3 = threading.Thread(name='nginx_obj',target=nginx_obj.run,args=())
            t3.start()

    def start(self):
        print('NginxManager prepare------', self.name)
        t = threading.Thread(target=self.run, name=self.name, args=())
        t.start()
        print('NginxManager start ------', self.name)


if __name__ == '__main__':
    print(random.randint(0,1))
