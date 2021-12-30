class header(object):
    def __init__(self):
        # flag:0 request 1: response
        self.flag = 0
        self.request_url = ['GET', '/', 'HTTP/1.2']
        # 通用首部
        self.common_info = {}
        # 请求首部
        self.request_info = {}
        # 响应首部
        self.response_info = {}
        # 实体首部
        self.enitity_info = {}
        # 扩展首部
        self.extend_info = {}
        # 所有首部
        self.all_info = {}
        # 首部清空
        self.clear()

    def clear(self):
        '''

        :return:
        '''
        # 通用首部
        self.common_info['Connection'] = None
        self.common_info['Date'] = None
        self.common_info['MIME-Version'] = None
        self.common_info['Trailer'] = None
        self.common_info['Transfer-Encoding'] = None
        self.common_info['Update'] = None
        self.common_info['Via'] = None
        ##通用缓存首部
        self.common_info['Cache-Control'] = None
        self.common_info['Pragma'] = None
        # 请求首部
        self.request_info['Client-IP'] = None
        self.request_info['From'] = None
        self.request_info['Host'] = None
        self.request_info['Referer'] = None
        self.request_info['UA-Color'] = None
        self.request_info['UA-CPU'] = None
        self.request_info['UA-Disp'] = None
        self.request_info['UA-OS'] = None
        self.request_info['UA-Pixels'] = None
        self.request_info['User-Agent'] = None
        ## Accept首部
        self.request_info['Accept'] = None
        self.request_info['Accept-Charset'] = None
        self.request_info['Accept-Encoding'] = None
        self.request_info['Accept-Language'] = None
        self.request_info['TE'] = None
        ## 条件请求首部
        self.request_info['Expect'] = None
        self.request_info['If-Match'] = None
        self.request_info['If-Modified-Since'] = None
        self.request_info['If-None-Match'] = None
        self.request_info['If-Range'] = None
        self.request_info['If-Unmodified-Since'] = None
        self.request_info['Range'] = None
        ## 安全请求首部
        self.request_info['Authorization'] = None
        self.request_info['Cookie'] = None
        self.request_info['Cookie2'] = None
        ## 代理请求首部
        self.request_info['Max-Forward'] = None
        self.request_info['Proxy-Authorization'] = None
        self.request_info['Proxy-Connection'] = None
        # 响应首部
        self.response_info['Age'] = None
        self.response_info['Public'] = None
        self.response_info['Retry-After'] = None
        self.response_info['Server'] = None
        self.response_info['Title'] = None
        self.response_info['Warning'] = None
        ## 协商首部
        self.response_info['Accept-Ranges'] = None
        self.response_info['Vary'] = None
        ## 安全响应首部
        self.response_info['Proxy-Authenticate'] = None
        self.response_info['Set-Cookie'] = None
        self.response_info['Set-Cookie2'] = None
        self.response_info['WWW-Authenticate'] = None
        # 实体首部
        self.enitity_info['Allow'] = None
        self.enitity_info['Location'] = None
        ## 内容首部
        self.enitity_info['Content-Base'] = None
        self.enitity_info['Content-Encoding'] = None
        self.enitity_info['Content-Language'] = None
        self.enitity_info['Content-Length'] = None
        self.enitity_info['Content-Location'] = None
        self.enitity_info['Content-MD5'] = None
        self.enitity_info['Content-Range'] = None
        self.enitity_info['Content-Type'] = None
        ## 实体缓存首部
        self.enitity_info['ETag'] = None
        self.enitity_info['Expires'] = None
        self.enitity_info['Last-Modified'] = None
        self.all_info.clear()

    def add_info(self, data: str):
        '''
        解析信息数据
        :param data:
        :return:
        '''
        data = data.strip()
        dats = data.split(":")
        size = len(dats)
        self.all_info[dats[0].strip()] = dats[1]
        for i in range(2,size):
            self.all_info[dats[0].strip()] += ':'+dats[i]
        self.all_info[dats[0].strip()] = self.all_info[dats[0].strip()].strip()



    def add_url(self, data: str):
        '''
        增加 URL
        :param data:
        :return:
        '''
        self.request_url = data.split(' ')
        method = self.request_url[0].lower()
        if method == 'get':
            self.flag = 0
        elif method == 'post':
            self.flag = 1
        elif method == 'put':
            self.flag = 2
        elif method == 'delete':
            self.flag = 3
        elif method == 'head':
            self.flag = 4
        else:
            self.flag = 5

    def string(self):
        '''
        打印所有首部
        :return:
        '''
        result = ""
        for key, value in self.all_info.items():
            if value is None:
                continue
            else:
                result += key + ": " + value + '\n'
        return result

    def string_flag(self):
        '''
        打印所对应的首部
        :return:
        '''
        result = ""
        for key, value in self.common_info.items():
            if value is None:
                continue
            else:
                result += key + ": " + value + '\n'
        if self.flag == 0:
            for key, value in self.request_info.items():
                if value is None:
                    continue
                else:
                    result += key + ": " + value + '\n'
        else:
            for key, value in self.response_info.items():
                if value is None:
                    continue
                else:
                    result += key + ": " + value + '\n'
        return result


if __name__ == '__main__':
    he = header()
    print(he.string())
    x = 'GET / HTTP/1.1'
    s = x.split(' ')
    print(s)
    buf = ''
    for ss in s:
        buf += ss + ' '
    print(buf)