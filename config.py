import math


class Strategy(object):
    '''
    策略模式
    '''

    def __init__(self):
        pass

    def strategy_run(self):
        pass


class Ip_Strategy(Strategy):
    '''
    IP 策略
    '''

    def __init__(self):
        super().__init__()

    def strategy_run(self):
        '''
        todo ip策略编写
        :return:
        '''
        pass


class Weight_Strategy(Strategy):
    '''
    Weight 策略
    '''

    def __init__(self, remote_addr, remote_url):
        super().__init__()
        self.record = []
        self.info = []
        self.remote_addr = remote_addr
        self.remote_url = remote_url
        for r_addr in remote_addr:
            self.record.append(r_addr[-1])
            self.info.append(r_addr[-1])

    def strategy_run(self):
        min_value = -math.inf
        min_index = -1
        for i in range(len(self.record)):
            if self.record[i] > min_value:
                min_value = self.record[i]
                min_index = i
        self.record[min_index] = self.record[min_index] - 1
        if self.record[min_index] < 0:
            self.record[min_index] = self.info[min_index]
        return self.remote_addr[min_index], self.remote_url[min_index]


class Config(object):
    '''
    存储配置数据的数据结构
    '''

    def __init__(self):
        self.local_port = 80
        self.local_url = '/'
        self.remote_addr = []
        self.remote_url = []
        self.loadbalance_strategy = 0
        self.info = {}
        self.strategy = None

    def set_strategy(self, strategy: Strategy):
        '''
        设置策略
        :param strategy: 输入策略
        :return:
        '''
        self.strategy = strategy

    def get_remote_info(self):
        '''
        根据策略获得ip地址，端口号，以及相对路径
        :return:
        '''
        return


def read_config_info(file_name) -> [str]:
    '''
    读取配置数据信息
    :param file_name:
    :return:
    '''
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
    '''
    处理单行数据
    :param line: 单行数据
    :return:
    '''
    line = line.strip()
    datas = line.split(' ')
    if len(datas) != 2:
        raise Exception('the pattern of configuration is not right')
    return datas


def str2list1(data: str) -> []:
    '''
    字符串转一维数组
    :param data:
    :return:
    '''
    result = []
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data.strip()
    dats = data.split(',')
    for dat in dats:
        result.append(dat.strip())
    return result


def str2list2(data: str) -> [[]]:
    '''
    字符传转二维数组
    :param data:
    :return:
    '''
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
    '''
    解析配置数据
    :param datas:
    :return:
    '''
    result = []
    temp = None
    for data in datas:
        data = str(data)
        if data.startswith('#'):
            continue
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
    '''
    配置文件读取以及解析步骤
    :return:
    '''
    datas = read_config_info('hginx.conf')
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
    # configs()
    x = "\nhello\n"
    # print(x)
    print(x.strip())
