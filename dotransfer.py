from makeT3Transfer_snu import *
import os

os.system("voms-proxy-init  cms")

user = "jalmond"
samples  = ["HNEE100"]

version = "LQ_Mar14"

path = "/data1/DATA/LQNtuples_5_3_14/MC/"
#path = "/data1/DATA/LQNtuples_5_3_14/Data/"

for s in samples:
    sample = version + s 
    endpath = path + s
    makeTransferFile_snu("cms2",sample, endpath, user )    
    os.system("rm -r "+ sample)
    
