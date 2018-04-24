# SNUNtupleT3Transfer

Runs in kisti. Before running setup root, either with CMSSW or root setup shell

After cloning branch run modify dotransferData_crab3_MC.py for your job and run:
python dotransferData_crab3_MC.py

The file copies from directries like: 

/xrootd/store/user/suoh/SKFlat/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/SKFlatMaker_2017_v1/180419_074221/000X/SKFlatNtuple_X.root

One file dotransferData_crab3_MC.py is used for each user, so if you copy files from suoh the lines in dotransferData_crab3_MC are:

file_user = "suoh"
samples  = [["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/","180419_074221"]]

This sample will copy TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8 with job stamp 180419_074221. It will copy all /0000/-/00XX/ directores

If no job stamp is given then the newest file is used


