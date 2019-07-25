from flask import Flask
from flask_restful import Resource, Api, abort
from datasource.crawler import Crawler, CrawlerStatus

app = Flask(__name__)
api = Api(app)
crawler = None

# API for managing crawler on the server
# parameter: action [start | pause | stop | status]
class CrawlerMgr(Resource):

    # compose status response
    def _return_status(self, crawler, msg_override=None):
        status, msg = crawler.status()
        # return status log message by default, unless overridden
        if msg_override is not None:
            msg = msg_override
        return {'status': status, 'message': msg}


    def get(self, action):

        # get global crawler handler
        global crawler
        if not crawler or not crawler.isAlive():
            crawler = Crawler()

        if action == 'start':
            if crawler.status()[0] == CrawlerStatus.IDLE:
                crawler.start()
                respond =  self._return_status(crawler)
            else:
                respond = self._return_status(crawler, msg_override='Crawler is already running.')

            return respond

        elif action == 'stop':
            if crawler.status()[0] == CrawlerStatus.RUNNING:
                crawler.stop()
                respond = self._return_status(crawler)
            else:
                respond = self._return_status(crawler, msg_override="Crawler is already stopped.")

            return respond

        elif action == 'status':
            return self._return_status(crawler)

        else:
            # invalid command, abort with 400
            abort(400)

api.add_resource(CrawlerMgr, '/crawler/<string:action>')

if __name__ == '__main__':
    app.run()
