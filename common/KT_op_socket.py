import socket

class op_socket:
    def __init__(self) -> None:
        self.sc_ip=None
        self.sc_port=None
        self.sc_bufsize=4096
        self.sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def sc_connet(self):
        sc_addr=(self.sc_ip,self.sc_port)
        self.sc.connect(sc_addr)
    def sc_bind(self):
        sc_addr=(self.sc_ip,self.sc_port)
        self.sc.bind(sc_addr)
        self.sc.listen(5)
    def sc_send(self,data):
        try:
            self.sc.send(data)
        except Exception as err:
            print (err)
    def sc_recv(self):
        return self.sc.recv(self.sc_bufsize)
    def sc_close(self):
        self.sc.close()

