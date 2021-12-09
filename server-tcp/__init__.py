import select,socket

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(('localhost',8087))
    server.listen(3)
    inputs = [server]
    outputs = []
    errors = []
    while len(inputs) > 0:
        reads,writes,exceptions = select.select(inputs,outputs,errors)
        for r in reads:
            if r == server:
                sock,addr = r.accept()
                print(addr)
                sock.setblocking(False)
                inputs.append(sock)
            else:
                buf = r.recv(1024)
                print(str(buf,encoding='utf-8'))
                outputs.append(r)
        for w in writes:
            w.send(bytes('have accepted',encoding='utf-8'))
            outputs.remove(w)


