from makeT3Transfer_snu import *
import os

os.system("voms-proxy-init  cms")
os.system("eval `ssh-agent`")
os.system("ssh-add")

######  DO NOT CHANGE

path = "/data1/DATA/LQNtuples_5_3_14_snu27/MC/"

#####  USER MUST CHANGE
user = "jalmond"

sigsamples  = ["40", "50", "60","70","80","90","100","125","150","175","200","225","250","275","300","325","350","375","400","500","600","700"]


for s in sigsamples:
    channel = ["EE","MuMu"]
    for c in channel:
        sigs = "MajoranaNeutrinoTo"+ c + "_M-"+ s + "_TuneZ2star_8TeV-alpgen"
        endpath = path + sigs
        makeTransferFile_snu("cms2",sigs, endpath, user, "LQNtupleSNU" )
        os.system("rm -r "+ sigs)
        
