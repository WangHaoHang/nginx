class Config(object):
    def __init__(self):
        self.local_port = 80
        self.local_url = '/'
        self.remote_addr = []
        self.remote_url = []
        self.loadbalance_strategy = 0
        self.info = {}


def read_config_info(file_name) -> [str]:
    fd = None
    try:
        fd = open(file_name, 'r')
        lines = fd.readlines()
        return lines
    except Exception as e:
        print('reading config exception happens:', e)
    finally:
        if fd != None:
            fd.close()


def pro_line(line: str):
    line = line.strip()
    datas = line.split(' ')
    if len(datas) != 2:
        raise Exception('the pattern of configuration is not right')
    return datas


def str2list1(data: str) -> []:
    result = []
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data.strip()
    dats = data.split(',')
    for dat in dats:
        result.append(dat.strip())
    return result


def str2list2(data: str) -> [[]]:
    results = []
    index_start = []
    index_end = []
    for i in range(len(data)):
        if data[i] == '[':
            index_start.append(i)
        if data[i] == ']':
            index_end.append(i)
    if len(index_start) != len(index_end):
        raise Exception("str2list2 happen Error!")
    for i in range(len(index_start) - 1):
        result = str2list1(data[index_start[i + 1]:index_end[i]])
        results.append(result)
    return results


def parse_config(datas: [str]) -> [Config]:
    result = []
    temp = None
    for data in datas:
        data = str(data)
        if data.startswith('start'):
            temp = Config()
            continue
        elif data.startswith('end'):
            result.append(temp)
            temp = None
            continue
        else:
            map_data = pro_line(data)
            key = map_data[0].strip().replace(':', '')
            value = map_data[1].strip()

        if data.startswith('local-port'):
            temp.local_port = int(value)
            temp.info[key] = temp.local_port
        elif data.startswith('local-url'):
            temp.local_url = value
            temp.info[key] = temp.local_url
        elif data.startswith('remote-url'):
            temp.remote_url = str2list1(value)
            temp.info[key] = temp.remote_url
        elif data.startswith('remote-addr'):
            temp.remote_addr = str2list2(value)
            temp.info[key] = temp.remote_addr
        else:
            temp.info[key] = value

    return result


def configs():
    datas = read_config_info('nginx.conf')
    configs_ = parse_config(datas)
    flag = 1
    for conf in configs_:
        print('configure ----', flag, '-----')
        print('local_port:', conf.local_port)
        print('local_url:', conf.local_url)
        print('remote_addr:', conf.remote_addr)
        print('remote_url:', conf.remote_url)
        print('info:', conf.info)
        flag += 1
    return configs_

if __name__ == '__main__':
    configs()
    # x = "hello"
