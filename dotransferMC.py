from makeT3Transfer_snu import *
import os

os.system("voms-proxy-init  cms")

######  DO NOT CHANGE

path = "/data1/DATA/LQNtuples_5_3_14_snu27/MC/"

#####  USER MUST CHANGE
user = "jalmond"
samples  = ["DYToEE_M-20_CT10_TuneZ2star_8TeV-powheg-pythia6" , "DYToMuMu_M-20_CT10_TuneZ2star_8TeV-powheg-pythia6" , "DYToTauTau_M-20_CT10_TuneZ2star_8TeV-powheg-pythia6" , "GluGluToHToZZTo4L_M-125_8TeV-powheg-pythia6", "TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola", "TTWJets_8TeV-madgraph","TTZJets_8TeV-madgraph_v2","WGToLNuG_TuneZ2star_8TeV-madgraph-tauola","WGstarToLNu2E_TuneZ2star_8TeV-madgraph-tauola","WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola","WWWJets_8TeV-madgraph","WW_DoubleScattering_8TeV-pythia8","WW_TuneZ2star_8TeV_pythia6_tauola","WZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola","WZJetsTo2QLNu_8TeV-madgraph","WZJetsTo3LNu_TuneZ2_8TeV-madgraph-tauola","WZ_TuneZ2star_8TeV_pythia6_tauola","WbbJetsToLNu_Massive_TuneZ2star_8TeV-madgraph-pythia6_tauola","WmWmqq_8TeV-madgraph","WpWpqq_8TeV-madgraph","ZGToLLG_8TeV-madgraph","ZZJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola","ZZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola","ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola","ZZTo2e2mu_8TeV-powheg-pythia6","ZZTo2e2tau_8TeV-powheg-pythia6","ZZTo2mu2tau_8TeV-powheg-pythia6","ZZTo4e_8TeV-powheg-pythia6","ZZTo4mu_8TeV-powheg-pythia6","ZZTo4tau_8TeV-powheg-pythia6","ZZ_TuneZ2star_8TeV_pythia6_tauola","ZbbToLL_massive_M-50_TuneZ2star_8TeV-madgraph-pythia6_tauola","WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball"]


for s in samples:

    endpath = path + s
    makeTransferFile_snu("cms2",s, endpath, user, "LQNtupleSNU")
    os.system("rm -r "+ s)
    


        
