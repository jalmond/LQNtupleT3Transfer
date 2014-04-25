from makeT3Transfer_snu import *
import os

os.system("voms-proxy-init  cms")

######  DO NOT CHANGE
path = "/data1/DATA/LQNtuples_5_3_14_snu27/Data/"

#####  USER MUST CHANGE
user = "jalmond"
#samples  = ["DiMuA" ,"DiMuB", "DiMuC", "DiMuD", "DiElA", "MuEGA", "MuA"]
samples  = ["DiElAV3", "DiElBV3", "DiElCV3", "DiElDV3"]
#samples  = ["DiElAV2"]

for s in samples:
    sample = version + s 
    endpath = path + s
    makeTransferFile_snu("cms2",sample, endpath, user )    
    os.system("rm -r "+ sample)
    
