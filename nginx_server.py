import socket, time
import threading

from nginx_struct import NginxObj, NginxManager
from config import configs,Config

def create_server(port: int) -> socket.socket:
    '''

    :param port:
    :return:
    '''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('localhost', port))
        # server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server.listen(5)
    except Exception as e:
        print("create Server is Error!")
        print("the exception is ", e)
    return server


if __name__ == '__main__':
    nginx_managers = []

    configs_ =configs()
    for config in configs_:
        nginx_manager = NginxManager()
        nginx_manager.add_config(config)
        nginx_manager.start()
        nginx_managers.append(nginx_manager)
