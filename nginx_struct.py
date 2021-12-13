import random
import socket, time
import threading
from multiprocessing import pool
from request_header import header
from config import Config
import logging


def transform_info(src_sock: socket.socket, dst_sock: socket.socket):
    '''
    将源头数据转发到目标源数据
    :param src_sock: 源 socket
    :param dst_sock:  目标 socket
    :return:  flag:True 调用成功， False:调用失败
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
        '''
        初始化
        :param src_sock: 源数据 -- socket
        :param dst_sock: 目标数据 -- socket
        :param config: 一个配置文件
        '''
        self.src_sock = src_sock
        self.dst_sock = dst_sock
        self.flag = True  # 是否结束 标志
        self.config = config
        self.head_info = header()  # 报文头部分析器、存储器
        self.xdata = ''  # 报文 body 部分
        self.orgin_context = ''  # 源数据
        self.select_index = 0  # 所选的映射下标

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
        获取所转换的报文数据，也是发给目标源的数据。
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
        转换源数据的头部信息，最后生成发送给目标源的头部信息
        :return:
        '''
        # 修改 Host
        remote_addr = str(self.config.remote_addr[self.select_index][0])
        if remote_addr.startswith('http'):
            self.head_info.all_info['Host'] = remote_addr.replace('http://', '')
        else:
            self.head_info.all_info['Host'] = remote_addr

        # 修改 request_url
        now_url = self.head_info.request_url[1]
        now_url = str(now_url)
        local_url = self.config.local_url
        remote_url = self.config.remote_url[self.select_index]
        print('url:', local_url, remote_url)
        if now_url.find(local_url) >= 0:
            if local_url == '/':
                if str(remote_url).endswith('/'):
                    self.head_info.request_url[1] = remote_url[0:-1] + now_url
                else:
                    self.head_info.request_url[1] = remote_url + now_url[1:]
            else:
                self.head_info.request_url[1] = now_url.replace(local_url, remote_url)
        print('request_url:', self.head_info.request_url[1])

    def send_str(self, sock: socket.socket, data: str):
        '''
        发送数据
        :param sock: 发送端
        :param data: 要发送的数据
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
        接收数据
        :param sock: 数据接受端
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
        数据转换
        :param src_sock: 源数据端口
        :param dst_sock: 目标数据端口
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
            if not self.flag:
                print(self.flag, getattr(self.src_sock, "_closed"), getattr(self.dst_sock, "_closed"))
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
        '''

        '''
        self.nginx_objs = []
        self.config = None
        self.server = None
        self.name = ''
        self.pool = pool.ThreadPool(10)

    def set_name(self, name: str):
        '''

        :param name:
        :return:
        '''
        self.name = name

    def add(self, nginx_obj: NginxObj):
        '''

        :param nginx_obj:
        :return:
        '''
        self.nginx_objs.append(nginx_obj)

    def add_config(self, config):
        '''

        :param config:
        :return:
        '''
        self.config = config

    def build_server(self):
        '''

        :return:
        '''
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(('localhost', self.config.local_port))
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.listen(5)
        except Exception as e:
            print("create Server is Error!")
            print("the exception is ", e)

    def remove_nginx(self):
        '''

        :return:
        '''
        pass

    def run(self):
        '''
        单线程运行
        :return:
        '''
        self.build_server()
        while True:
            src_socket, addr = self.server.accept()
            print('accept:', addr)
            dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            '''
                先写一个随机选择算法
            '''
            size = len(self.config.remote_addr)
            index = random.randint(0, size - 1)
            # print('index:',index)
            # index = size - 1
            print('addr:', (self.config.remote_addr[index][0], int(self.config.remote_addr[index][1])))
            dst_socket.connect((self.config.remote_addr[index][0], int(self.config.remote_addr[index][1])))
            nginx_obj = NginxObj(src_socket, dst_socket, config=self.config)
            nginx_obj.select_index = index
            self.nginx_objs.append(nginx_obj)
            self.pool.apply_async(func=nginx_obj.run,args=())

    def start(self):
        '''
        单线程开启
        :return:
        '''
        print('NginxManager prepare------', self.name)
        t = threading.Thread(target=self.run, name=self.name, args=())
        t.start()
        print('NginxManager start ------', self.name)


if __name__ == '__main__':
    print(random.randint(0, 1))
    logging.error('hello - %s', 'world')
    pool_ = pool.ThreadPool()

