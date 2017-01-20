from web.basehandler import BaseHandler


class ComputeHandler(BaseHandler):

    def get(self):
        self.queue.put(True)
        self.write('Queued')