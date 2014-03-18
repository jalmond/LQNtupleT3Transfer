from makeT3Transfer_snu import *
import os

user = "jalmond"
samples  = ["HNEE100" , "HNEE125", "HNEE150", "HNEE175", "HNEE200", "HNEE225", "HNEE250", "HNEE275," "HNEE300", "HNEE325", "HNEE350", "HNEE375", "HNEE400", "HNEE50", "HNEE500", "HNEE600", "HNEE70", "HNEE700", "HNEE90" ]

version = "LQ_Mar14"
path = "/data1/DATA/LQNtuples_5_3_14/MC/"
#path = "/data1/DATA/LQNtuples_5_3_14/Data/"

for s in samples:
    sample = version + s 
    endpath = path + s
    makeTransferFile_snu("cms2",sample, endpath, user )    

    
