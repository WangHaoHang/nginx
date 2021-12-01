class header(object):
    def __init__(self):
        self.request_url=['GET','/','HTTP/1.2']
        #通用首部
        self.common_request_info = {}
        #请求首部
        self.request_info = {}
        #
        self.response_info = {}
        self.enitity_info ={}
    def string(self):
        pass
if __name__ == '__main__':
    pass