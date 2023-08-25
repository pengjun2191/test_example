import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from locust import  TaskSet, task,between,events,FastHttpUser
from gevent._semaphore import Semaphore


all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()# 阻塞线程


def on_hatch_complete(**kwargs):
    """
    Select_task类的钩子方法
    :param kwargs:
    :return:
    """
    all_locusts_spawned.release() # # 创建钩子方法


events.spawning_complete.add_listener(on_hatch_complete) #挂在到locust钩子函数（所有的Locust示例产生完成时触发）


n = 0
class UserBehavior(TaskSet):

    def login(self):
        global n
        n += 1
        print("%s个虚拟用户开始启动，并登录"%n)

    def logout(self):
        print("退出登录")



    def on_start(self):
        self.login()

        all_locusts_spawned.wait() # 同步锁等待

    @task(96)
    def test1(self):
        url = '/upp/login.jsp'
        with self.client.get(url,headers={},catch_response = True) as response:
            print(response)
            print("登录首页")

    def on_stop(self):
        self.logout()

class WebsiteUser_fast(FastHttpUser):
    host = 'http://www.baidu.com'
    tasks = [UserBehavior]

    wait_time = between(1, 2)




if __name__ == '__main__':
    os.system("locust -f locustfile_fasthttp.py --worker")
