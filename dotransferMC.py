from makeT3Transfer_snu import *
import os

os.system("voms-proxy-init  cms")

######  DO NOT CHANGE
version = "LQ_Mar14"
path = "/data1/DATA/LQNtuples_5_3_14/MC/"

#####  USER MUST CHANGE
user = "jalmond"
samples  = ["ttbar", "QCD_30to40EE", "QCD_40EE", "Wgamma", "ZZ", "WW", "WZ", "SSWpWp","SSWmWm","WW_ds", "TTZ", "TTW", "WWW","DY10to50","DY50plus"]

for s in samples:
    sample = version + s 
    endpath = path + s
    makeTransferFile_snu("cms2",sample, endpath, user )    
    os.system("rm -r "+ sample)
    
