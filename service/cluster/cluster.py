import numpy as np
import pandas as pd
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
from sklearn.preprocessing import LabelEncoder

class Cluster:
    def __init__(self, df):
        # pre processing, prepare two features: connections & Location
        # clean and drop redundant columns
        self.df = df
        self.df['Connection'] = self.df['Connection'].replace('500+', '500')
        self.df = self.df.loc[0:, ['Location', 'Connection']].reset_index(drop=True)

        #Encode
        enc = LabelEncoder()
        self.df = self.df.apply(enc.fit_transform)

    def meanShift(self):
        # The following bandwidth can be automatically detected using
        bandwidth = estimate_bandwidth(self.df)
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(self.df)
        labels = ms.labels_

        # add group labels
        self.df['group'] = pd.Series(labels)

        return self.df.to_dict('records')

    def kMeans(self):
        km = KMeans(n_clusters=5)
        km.fit(self.df)
        labels = km.labels_

        # add group labels
        self.df['group'] = pd.Series(labels)

        return self.df.to_dict('records')
