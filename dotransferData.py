from makeT3Transfer_snu import *
import os

os.system("voms-proxy-init  cms")

######  DO NOT CHANGE
version = "LQ_Mar14"
path = "/data1/DATA/LQNtuples_5_3_14/Data/"

#####  USER MUST CHANGE
user = "jalmond"
samples  = ["DiMuA"] 

for s in samples:
    sample = version + s 
    endpath = path + s
    makeTransferFile_snu("cms2",sample, endpath, user )    
    os.system("rm -r "+ sample)
    
