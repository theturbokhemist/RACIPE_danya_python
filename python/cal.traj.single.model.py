#/usr/bin/env python
''''
    racipe: this program implements the RACIPE method to generate an 
ensemble of network models from a given gene network topology. 
    How to run this tool?
    Mode 1: topology mode-supply only topology file-
       > python racipe.py -M='T' \
                          -I1=TS.tpo \
     Mode 2: parameter mode-supply parameter file as well-
       > python racipe.py -M='C' \
                          -I1=TS.tpo \
                          -I2=TS.prs \
'''
import os
import sys

CUR_DIR=os.getcwd()
PROG_PATH=os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(PROG_PATH)
import networkManager as nm 
import modelGenerator as mg 
import dataAnalyzer as da 
import modelAnalyzer as ma

from collections import defaultdict 
from collections import OrderedDict
import time
from os.path import basename 

def are_seeds_valid(USER_SEED, SEED):
    if (int(USER_SEED)<=0 and int(SEED)<=0):
        return False 
    return True 

#======================================================================#
def main():

    import numpy as np

    # create an instance of Network class: 
    network=nm.Network(CUR_DIR) 

    config_dict=network.get_config_dict()

    SEED=int(config_dict['SEED'])
    USER_SEED=int(config_dict['USER_SEED'])

    #load network topology and parameter ranges:
    mode=network.process_network(USER_SEED, SEED)

    #MODEL_DIR = "/Users/kateba/research/cellcycle.suppl/data-raw/earlyG1-midG1/"
    MODEL_DIR = "/Users/kateba/research/cellcycle.suppl/repressilator/tdynamics/phase.01/"
    fname_params = MODEL_DIR + 'repressilator.params.txt'
    fname_models = MODEL_DIR + 'model_list.txt'
    print(fname_params)

    # import the model ids:
    #fh_models = open(fname_models, 'r') 
    #line = fh_models.readline()
    #fields = line.strip().split()
    #MODELS_TO_INSPECT = list(map(int, fields))

    # import model ids from the input file:
    with open(fname_models, 'r') as fh_models: 
        content = fh_models.read()
    models = content.strip().split("\n")

    MODELS_TO_INSPECT = list(map(int, models))

    model_params_dict = ma.import_model_params(open(fname_params, "r"), \
                                            network, MODELS_TO_INSPECT)

    model_list = list(model_params_dict.keys())
    print(model_list)

    cur_model = model_list[0]

    params_list = model_params_dict[cur_model]
    #MPR_arr = params_list[0]
    #DNR_arr = params_list[1]
    #TSH_arr = params_list[2]
    #HCO_arr = params_list[3]
    #FCH_arr = params_list[4]

    # Create parameter variables with values assigned: 
    MPR_arr = np.array([50.00, 50.00, 50.00])
    DNR_arr = np.array([0.10, 0.10, 0.10])
    TSH_arr = np.array([100.00, 100.00, 100.00])
    HCO_arr = np.array([3.00, 3.00, 3.00])
    FCH_arr = np.array([10.00, 10.00, 10.00])
    params_list = [MPR_arr, DNR_arr, TSH_arr, HCO_arr, FCH_arr]

    for cur_model in model_list:
        print(cur_model)
        #params_list = model_params_dict[cur_model]
        ma.cal_time_traj(network, cur_model, params_list)
        break
 
    return None 

#**********************************************************************#
if __name__=='__main__':
   start_time=time.time()
   main()
   os.chdir(CUR_DIR)
   print("--- %s seconds ---" % (time.time() - start_time))
