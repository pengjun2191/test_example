from zeep import Client
class op_webservice:
    def __init__(self,url):
        self.url=url
    def create_client(self):
        self.client=Client(self.url)
        return self.client
    def get_result(self):
        pass

if __name__=="__main__":
    pass
