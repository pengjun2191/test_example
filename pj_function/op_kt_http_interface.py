import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
import httpx
from pj_function.get_kt_http_interface_data import target_queue
from pj_function.get_config import get_config
import threading

cfg=get_config()
async def post_result(url,json_str):
    async with httpx.AsyncClient() as client:
        await client.post(url,json=json_str)

async def get_result(url):
    async with httpx.AsyncClient() as client:
        await client.get(url)

class  myThread(threading.Thread):
   def __init__(self, threadID, name, q):
       threading.Thread.__init__(self)
       self.threadID = threadID
       self.name = name
       self.q = q
       
   def run(self):
       print("Thread Start: "+ self.name)
       process_data(self.name, self.q)
       print("Thread Exit: "+ self.name)
       
def process_data(threadName, data):
   while not exitFlag:
        queueLock.acquire()
        url=f"http://{cfg.httpurl['host']}:{cfg.httpurl['port']}{cfg.httpurl['url']}"
        try:
            if not data_queue.empty():
                asyncio.run(post_result(url,data.get_nowait()))
                print(data.qsize())
                queueLock.release()
                print("{} processing {}".format(threadName, data))
            else:
                queueLock.release()
        except Exception as e:
            print(e)
            print("发送完成")

def send_100_http(data):
    url="http://www.baidu.com"
    loop = asyncio.get_event_loop()
    task = [get_result(url) for i in range(100)]  # 把任务放入数组,准备给事件循环器调用
    loop.run_until_complete(asyncio.wait(task))
    loop.close()

def send_http_thread(data,num=3):
    global exitFlag,queueLock
    exitFlag=0
    # 创建锁
    queueLock = threading.Lock()
    threads = []
    threadID =1
    for i in range(1,num+1):
    # 创建新线程
        thread = myThread(threadID, f"Thread-{i}", data)
        thread.start()
        threads.append(thread)
        threadID +=1
 
    # 等待队列清空
    while not data_queue.empty():
        pass
 
    # 通知线程退出
    exitFlag =1
 
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("exit")

if __name__=="__main__":
    data_queue=target_queue()
    send_http_thread(data_queue)
    
 

    
        



