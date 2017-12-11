from __future__ import division
import scipy
import os
import sys;
import utils;
import csv;
import collections
import numpy as np
import itertools
from utils.read_data import readAdjInterceptFile
from utils.read_data import readRawTurkDataFile
from utils.read_data import readWithSpace
import pickle as pk
from scipy.stats import kendalltau, spearmanr
from utils.linearReg import runLR

import time

from utils.grounding import predict_grounding
from utils.grounding import get_features_y
from utils.squish import run_adj_emb

start_time = time.time()

cwd=os.getcwd()
turkFile="adjectiveData.csv"
turkInterceptFile="turk_with_intercept.txt"

if __name__ == "__main__":
    try:





        features, y, adj_lexicon= get_features_y(cwd, turkFile,False)

        print(features.shape)

        #get the 300 embedding vector from glove for an adj
        run_adj_emb(features,y,adj_lexicon)


        adj_lexicon_flipped = dict()
        #total number of unique adjectives
        num_adj = len(adj_lexicon)

        #key=index value=adjective
        for a, idx in adj_lexicon.items():
            adj_lexicon_flipped[idx] = a

        #actual linear regression part- how much weight should it assigne to each of 1-hot-adj-vector, mean and variance

        #will be of size 1x100=98 adj, one mean and variance
        learned_weights = runLR(features, y)

        print(str(learned_weights.shape))
        #sys.exit(1)
        #print("NumUniqueAdj: ", num_adj)
        # Get the weights that correspond to the individual adjs
        adj_intercepts_learned = learned_weights[:num_adj]
        #pairing weights with adjectives.
        adj_pairs = [(learned_weights[0][i], adj_lexicon_flipped[i]) for i in range(num_adj)]

        #print(adj_pairs[:2])

        #sorting them by their weight
        sorted_adjs = sorted(adj_pairs, key=lambda x: x[0], reverse=True)

        #print highest 20 intercepts and lowest 20 intercepts
        print(sorted_adjs[:20])
        print(sorted_adjs[-20:])


        #get the actual intercepts
        # adj_intercepts_original=readWithSpace(cwd,turkInterceptFile)
        # print((adj_intercepts_original["adjective"][0]))
        # # print((adj_intercepts_original["intercept"][0]))
        # print(str(adj_intercepts_original.shape))
        # print(str(adj_intercepts_learned.shape))
        #sys.exit(1)




        # features,y =predict_grounding(cwd,turkFile)
        # print("size of features is:")
        # print((features.shape))
        # print("size of y is:")
        # print((y.shape))

    ##################################end of dev phase####################
    except:
        import traceback
        print('generic exception: ' + traceback.format_exc())
        elapsed_time = time.time() - start_time
        print("time taken:" + str(elapsed_time))






