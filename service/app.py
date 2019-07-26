from flask import Flask
from flask_restful import Resource, Api, abort
from flask_cors import CORS
from datasource.crawler import Crawler, CrawlerStatus
from cluster.cluster import Cluster
import csv
import pandas as pd

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

crawler = None
filename = {'demo':'sample_results.csv', 'crawled':'results.csv', 'connection':'connection.csv'}


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


# API for serving raw dataset
# parameter: dataset [demo | crawled | connection]
#   - demo:         Pre crawled data for demo use
#   - crawled:      Freshly crawled data
#   - connection:   1st connections of the user (oauth required) *NOT TESTED*
class DatasetSrv(Resource):

    def get(self, dataset):

        if dataset in filename:
            try:
                with open('results/' + filename[dataset]) as f:
                    reader = csv.reader(f)
                    return {'status': 0, 'data':list(reader)}
            except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
                return {'status': 1, 'data':'Dataset not ready or does not exist.'}

        else:
            # invalid dataset
            return {'status': 1, 'data':'Invalid dataset.'}


# API for serving clustered data
# parameter: dataset [demo | crawled | connection]
#   - demo:         Pre crawled data for demo use
#   - crawled:      Freshly crawled data
#   - connection:   1st connections of the user (oauth required) *NOT TESTED*
# parameter: method [kmeans | meanshift]
class ClusterSrv(Resource):

    def get(self, dataset, method):
        if method not in ['kmeans', 'meanshift']:
            # invalid command, abort with 400
            abort(400)

        if dataset not in filename:
            # invalid dataset
            return {'status': 1, 'data': 'Invalid dataset.'}

        try:
            df = pd.read_csv('results/' + filename[dataset])
            cluster = Cluster(df)
            result = None
            # dispatch to corresponding cluster method
            if method == 'meanshift':
                result = cluster.meanShift()
            elif method == 'kmeans':
                result = cluster.kMeans()
            return {'status': 0, 'data': result}

        except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
            return {'status': 1, 'data': 'Dataset not ready or does not exist.'}


api.add_resource(CrawlerMgr, '/crawler/<string:action>')
api.add_resource(DatasetSrv, '/dataset/<string:dataset>')
api.add_resource(ClusterSrv, '/cluster/<string:dataset>/<string:method>')

if __name__ == '__main__':
    app.run()
