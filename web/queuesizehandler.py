from web.basehandler import BaseHandler


class QueueSizeHandler(BaseHandler):

    def get(self):
        self.write('%d' % self.queue.qsize())
