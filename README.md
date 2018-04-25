# SNUNtupleT3Transfer

Runs in kisti. Before running setup root, either with CMSSW or root setup shell

After cloning branch run modify dotransferData_crab3_MC.py for your job by changing
Change user_name="XX" in dotransferData_crab3_DATA.py or dotransferData_crab3_MC.py

Can run samlpes from googledoc:
https://docs.google.com/spreadsheets/d/1TedFWvlM3XW1184wwuqgzXKX7OCO1Nneo2eHT0amsvk/edit#gid=0

Or manual (change manualConfiguration=False -> manualConfiguration=True)


For new versions of SKFLat tags: 

In makeT3Transfer_snu_crab3.py update GetFromGoogleDoc function to include new url, which is for tab in googkedoc:

For example: 
if tag == "SKFlat_v944_3":
     url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSgwHJjUyFC1Ck2ewgajQhf14as-tKZEQsofwh0UlJo3fPlXSh8S85sHnDtsWgwu5qTkqwyAKb8wjJu/pub?gid=0&single=true&output=csv'

in dotransferData_crab3_XXX.py: 

update SKtag="SKFlat_v944_3"
and if needed:
path = "/data8/DATA/SKFlat/v9-4-4/DATA/"


