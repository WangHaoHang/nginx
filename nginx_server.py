import socket, time
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
    server = create_server(8088)
    nginx_manager = NginxManager()
    configs_ =configs()
    while True:
        src_socket, addr = server.accept()
        dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dst_socket.connect((configs_[0].remote_addr[0][0], int(configs_[0].remote_addr[0][1])))
        nginx_obj = NginxObj(src_socket, dst_socket,config=configs_[0])
        nginx_manager.add(nginx_obj)
        nginx_obj.run()
