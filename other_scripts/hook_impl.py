class ContentStash(object):

    def __init__(self):
        self.input_filter_fn = None
        self.broker = []

    def register_input_filter_hook(self, input_filter_fn):

        self.input_filter_fn = input_filter_fn

    def insert_queue(self, content):

        self.broker.append(content)

    def input_pipeline(self, content, use=False):
        if not use:
            return

        # input filter
        if self.input_filter_fn:
            _filter = self.input_filter_fn(content)
            
        # insert to queue
        if not _filter:
            self.insert_queue(content)



# test
## 实现一个你所需要的钩子实现：比如如果content 包含time就过滤掉，否则插入队列
def input_filter_hook(content):

    if content.get('aaa') is None:
        return
    else:
        return content


if __name__=="__main__":
    # 原有程序
    content = {'filename': 'test', 'test': "test"}
    content_stash = ContentStash()

    # 挂上钩子函数， 可以有各种不同钩子函数的实现，但是要主要函数输入输出必须保持原有程序中一致，比如这里是content
    content_stash.register_input_filter_hook(input_filter_hook)

    # 执行流程
    content_stash.input_pipeline(content,True)
    print(content_stash.broker)