import queue
class get_rt_data:
    def __init__(self) -> None:
        self.rt_ip=None
        self.rt_port=None
        self.rt_bufsize=4096
        self.data=queue.Queue()
    def pack_data(self):
        pass
    def get_data_num(self):
        """返回队列长度"""
        return self.data.qsize()
    