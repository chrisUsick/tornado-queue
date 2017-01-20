import tornado
from tornado import web, queues, ioloop
from tornado.gen import sleep
from tornado.ioloop import IOLoop

from web.computehandler import ComputeHandler
from web.queuesizehandler import QueueSizeHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

queue = queues.Queue()
concurrency = 2
async def work():
    print('starting work')
    while True:
        v = await queue.get()
        print('work got')
        await sleep(10)
        queue.task_done()
        print('did work on %s' % v)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/compute", ComputeHandler),
            (r"/queue/size", QueueSizeHandler)
        ]
        super(Application, self).__init__(handlers)

    def work_queue(self):
        return queue


async def main():
    for _ in range(concurrency):
        IOLoop.current().spawn_callback(work)
    print('started main')


if __name__ == "__main__":

    application = Application()
    application.listen(8888)
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.run_sync(main)
    io_loop.start()

