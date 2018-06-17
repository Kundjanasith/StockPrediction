# coding: utf-8

import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import pylab

from MultiLoader import MultiLoader



def load_data(date_file, stock_data_files):
    """
    Scraper が吐き出したファイルを読むのです。
    日付と調整後終値を返すのです。
    """
    multi_loader = MultiLoader(date_file, stock_data_files)
    adj_ends = multi_loader.extract('adj_end')
    # adj_ends = multi_loader.extract('ommyo_log')
    # adj_ends = multi_loader.extract('ommyo_rate')
    return adj_ends


def rate_of_decline(values):
    ret_val = pd.Series(values).pct_change()
    return ret_val[1:]


if __name__ == '__main__':

    stock_data_files = [
        ',Nikkei225.txt', ',TOPIX.txt', ',6501.txt', ',7238.txt', ',8306.txt', ',8411.txt'
    ]
    date_file = ',date.txt'

    adj_ends = load_data(date_file, stock_data_files)

    for (i, stock) in enumerate(stock_data_files):
        # 変化率を出す
        print(stock, i)
        rod = rate_of_decline(adj_ends[i])
        # rod = adj_ends[i]

        pylab.clf()
        pylab.hist(rod, bins=50, rwidth=0.8)
        pylab.savefig(',LSTM4Histogram%s.png' % (stock))

        stdev = np.std(rod)
        print('stdev', stdev)

        threshold = 0.010
        categorized = pd.cut(rod, [-1, -threshold, 0, threshold, 1])
        # categorized = pd.qcut(rod, 4)
        # print(categorized)
        count = categorized.value_counts()
        print(count)
