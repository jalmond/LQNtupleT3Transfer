from makeT3Transfer_snu import *
import os

os.system("voms-proxy-init  cms")

######  DO NOT CHANGE
path = "/data1/DATA/LQNtuples_5_3_14_snu27/Data/"

#####  USER MUST CHANGE
user = "jalmond"
samples  = ["DoubleElectron", "DoubleMu","DoubleMuParked"]

for s in samples:
    
    endpath = path + s
    makeTransferFile_snu("cms2",s, endpath, user ,"LQNtupleSNU_data")    
    os.system("rm -r "+ s)
    
