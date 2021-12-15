import socket, time
import threading
import random
from nginx_struct import NginxObj
from config import configs, Config
from concurrent.futures import ThreadPoolExecutor

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
        self.pool = ThreadPoolExecutor(max_workers=10)
        self.flag = True
        self.tasks = []

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
        建立 server-socket
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
        while self.flag:
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
            task = self.pool.submit(nginx_obj.run)
            self.tasks.append(task)
    def start(self):
        '''
        单线程开启
        :return:
        '''
        print('NginxManager prepare------', self.name)
        t = threading.Thread(target=self.run, name=self.name, args=())
        t.start()
        print('NginxManager start ------', self.name)

    def stop(self):
        print('NginxManager stop-------', self.name)
        self.flag = False



if __name__ == '__main__':
    nginx_managers = []

    configs_ = configs()
    flag = 0
    for config in configs_:
        nginx_manager = NginxManager()
        nginx_manager.add_config(config)
        nginx_manager.set_name('manager' + str(flag))
        nginx_manager.start()
        nginx_managers.append(nginx_manager)
        flag += 1
