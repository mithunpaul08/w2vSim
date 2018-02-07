from __future__ import division
import scipy
import os
import sys;
import utils;
import csv;
import collections
import numpy as np
import itertools
import pickle as pk
import time

from utils.grounding import predict_grounding
from utils.grounding import get_features_dev
from utils.grounding import get_features_training_data
from utils.grounding import split_data_based_on_adj


from utils.squish import do_training
from utils.squish import run_loocv_on_turk_data
from utils.squish import run_nfoldCV_on_turk_data
from utils.squish import run_loocv_per_adj
from utils.squish import tuneOnDev
from utils.squish import train_dev_print_rsq
from utils.squish import cutGlove
from utils.squish import runOnTestPartition

from utils.read_write_data import writeCsvToFile
from utils.read_write_data import writeDictToFile
from sklearn.metrics import r2_score
from utils.read_write_data import readAdjInterceptFile
from utils.read_write_data import readRawTurkDataFile
from utils.read_write_data import readWithSpace
from utils.squish import predictAndCalculateRSq
from scipy.stats import kendalltau, spearmanr
from utils.linearReg import runLR


start_time = time.time()

cwd=os.getcwd()
entire_turk_data="all_turk_data.csv"
dev="dev.csv"
training_data="trainingData.csv"
turkInterceptFile="turk_with_intercept.txt"
test_data="test.csv"

dev_adj="dev_adj.csv"
training_adj="trainingData_adj.csv"
test_adj="test_adj.csv"

addTurkerOneHot=False
addAdjOneHot=False
useEarlyStopping=True

rsq_on_test="rsq_on_test.txt"

if __name__ == "__main__":
    try:





        while True:
                print("                      ")
                print("          ******            ")

                print("Welcome to Grounding For Adjectives. Please pick one of the following:")

                print("To run the model with just linear regression Press:1")
                print("To train the model with a dense NN+embeddings and save the model 80-10-10:2")
                print("To test the model with a dense NN saved best model 80-10-10:3")
                print("To exit Press:0")


                myInput=input("what is your choice:")

                uniq_turker = {}

                if(myInput=="2"):



                    #get the embeddings for only the adjectives we need and write it to a file
                    # cut_glove=cutGlove(adj_lexicon);
                    # writeDictToFile(cut_glove,cwd,"glove_our_adj")
                    # sys.exit(1)




                    #run1: run with leave one out cross validationon all the turk experiment data points-i.e no adjective based split
                    # read all the data. i.e without training-dev-split. This is for LOOCV
                    #features, y, adj_lexicon, all_adj, uniq_turker,uniq_adj_list = get_features_training_data(cwd, entire_turk_data,
                                                                                               #addAdjOneHot, uniq_turker,addTurkerOneHot)

                     # run1: run with leave one out cross validation
                    #run_nfoldCV_on_turk_data(features, y, adj_lexicon, all_adj,addTurkerOneHot,useEarlyStopping)

                    print("done loocv for all turk data, going to exit")


                    #run 2 : do training and dev tuning separately--this is entire data, not based on adjectives.
                    # readtraining data
                    # uniq_turker = {}
                    # features, y, adj_lexicon, all_adj, uniq_turker = get_features_training_data(cwd, training_data,
                    #                                                                             False, uniq_turker)
                    # trained_model=do_training(features, y, adj_lexicon, all_adj)
                    # # test on dev data
                    # tuneOnDev(cwd, dev, False, uniq_turker)



                    # run 3: run both dev and training together and print rsq after each epoch
                    # mutual exclusive with run 2 above



                    #code that splits the data based on adjectives and not the entire data- should be used only once ideally
                    # features, y, adj_lexicon, all_adj, uniq_turker = split_data_based_on_adj(cwd, entire_turk_data,
                    #                                                                          False, uniq_turker)

                    features, y, adj_lexicon, all_adj, uniq_turker,uniq_adj_list = get_features_training_data(cwd, training_adj,
                                                                                               addAdjOneHot, uniq_turker,addTurkerOneHot)

                    #train on the adj based training split and tune on dev. All is done inside train_dev_print_rsq
                    trained_model = train_dev_print_rsq(dev_adj,features, y, adj_lexicon, all_adj,uniq_turker,addTurkerOneHot)
                    print("done training and tuning on dev . Going to  test on test data")

                    #instead of splitting data into 80-10-10, do LOOCV based on adjectives
                    #run_loocv_per_adj(features, y, adj_lexicon, all_adj,addTurkerOneHot,uniq_adj_list)



                    print("done loocv for adj based turk data, going to exit")



                    adj_lexicon_flipped = dict()
                    #total number of unique adjectives
                    num_adj = len(adj_lexicon)

                    #key=index value=adjective
                    for a, idx in adj_lexicon.items():
                        adj_lexicon_flipped[idx] = a


                    # features, y, adj_lexicon,all_adj=  get_features_dev(cwd, dev,False,uniq_turker)
                    # print("done reading dev data:")


                    #############use the trained model to test on test split






                    # adj_intercepts_learned = learned_weights[:num_adj]
                    # #pairing weights with adjectives.
                    # adj_pairs = [(learned_weights[0][i], adj_lexicon_flipped[i]) for i in range(num_adj)]

                    # sorted_adjs = sorted(adj_pairs, key=lambda x: x[0], reverse=True)
                    #
                    # #print highest 20 intercepts and lowest 20 intercepts
                    # print(sorted_adjs[:20])
                    # print(sorted_adjs[-20:])
                    elapsed_time = time.time() - start_time
                    print("time taken:" + str(elapsed_time/60)+"minutes")

                else:
                    if(myInput=="3"):

                        #empty out the existing file
                        with open(cwd + "/outputs/" + rsq_on_test, "w+")as rsq_values:
                            rsq_values.write("Epoch \t Train \t\t Dev \n")
                            rsq_values.close()

                        #append the rest of the values
                        with open(cwd+"/outputs/" +rsq_on_test,"a")as rsq_values:

                            trained_model = pk.load( open( "all_data_80-10-10.pkl", "rb" ))
                            runOnTestPartition(trained_model,test_data,cwd, uniq_turker,rsq_values,addTurkerOneHot,1)



                            # features, y, adj_lexicon,all_adj= get_features_y(cwd, turkFile,False)
                            # adj_lexicon_flipped = dict()
                            # #total number of unique adjectives
                            # num_adj = len(adj_lexicon)
                            #
                            # #key=index value=adjective
                            # for a, idx in adj_lexicon.items():
                            #     adj_lexicon_flipped[idx] = a
                            #
                            #
                            # #run with leae one out cross validation
                            # run_loocv_on_turk_data(features, y, adj_lexicon, all_adj)

                            #run just with a classic train-dev-test partition
                            elapsed_time = time.time() - start_time
                            print("time taken:" + str(elapsed_time/60)+"minutes")
                    else:
                        if(myInput=="0"):
                            print("******Good Bye")
                            break;
                        else:
                            if(myInput=="1"):

                                features, y, adj_lexicon,all_adj= get_features_y(cwd, turkFile,False)
                                print(features.shape)

                                adj_lexicon_flipped = dict()
                                #total number of unique adjectives
                                num_adj = len(adj_lexicon)

                                #key=index value=adjective
                                for a, idx in adj_lexicon.items():
                                    adj_lexicon_flipped[idx] = a

                                #actual linear regression part- how much weight should it assigne to each of 1-hot-adj-vector, mean and variance

                                #will be of size 1x100=98 adj, one mean and variance
                                learned_weights = runLR(features, y)

                                #print(str(learned_weights.shape))
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

    ##################################end of dev phase####################
    except:
        import traceback
        print('generic exception: ' + traceback.format_exc())
        elapsed_time = time.time() - start_time
        print("time taken:" + str(elapsed_time))






