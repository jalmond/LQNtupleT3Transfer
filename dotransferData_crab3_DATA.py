from makeT3Transfer_snu_crab3 import *
import os,time

#This script will copy files in kisti to SNU. It only copies files completly copied from grid, and then once all finished will check that files were successfully copied to SNU, if not it will repeat the copy. Then after time "k_sleep" it will check if new files are ytransferred from crab and copy only these files.

#check screen is running 
print "Currently using screen ssh to allow access: " 
user_name="jalmond"
snu_ip="147.47.242.42"
CheckSetup(user_name,snu_ip)

######  DO NOT CHANGE without dsicussing with all, as this is path for samples 
path = "/data8/DATA/SKFlat/v9-4-4/DATA/"
SKtag="SKFlat_v944_3"


#####  USER MUST CHANGE, this is list for jobs 



## in samples second argument is the time tag of directory, if empty newest directory is used                                                                                                                                           

manualConfiguration=False ### set true if you dont want to copy all samples from googledoc
samples = GetFromGoogleDoc(SKtag, manualConfiguration, True)


if len(samples) == 0 :
    job_file_user = "jskim"
    samples  =  [["DoubleMuon","180424_000041","periodB",job_file_user],
                 ["DoubleMuon","180424_000131","periodC",job_file_user],
                 ["DoubleMuon","180424_000221","periodD",job_file_user],
                 ["DoubleMuon","180424_000310","periodE",job_file_user],
                 ["DoubleMuon","180424_000358","periodF",job_file_user]]
    

##### This is for general job configuration
k_sleep=120 # number of seconds to wait before rerunning script to pick up new files finished 

rerun_samples=[]
complete_samples=[]

n_runs=0
while not len(complete_samples) == len(samples):
    print "Iteration ("+str(n_runs)+"):"
    if n_runs >20:
        print "Ran script for 20 iterations, will exit for now."
        quit()

    if n_runs > 0:
        time.sleep(k_sleep)
    for s_all in samples:    
        s=s_all[0]
        s_orig=s
        completed=False
        for cs in complete_samples:
            if cs == s:
                completed=True
        if completed:
            continue
        s_tag=s_all[1]
        period=s_all[2]
        file_user=s_all[3]
        if "/" in s:
            s=s.replace("/","")
    
        print "Sample : " + s + " tag= " + s_tag
        os.system("ssh "+user_name+"@" + snu_ip + " 'mkdir " + path+"/"+SKtag + "'")
        os.system("ssh "+user_name+"@" + snu_ip + " 'mkdir " + path+"/"+SKtag +"/DATA/"+ "'")
        os.system("ssh "+user_name+"@" + snu_ip + " 'mkdir " + path+"/"+SKtag +"/DATA/"+ s +"'")
        os.system("ssh "+user_name+"@" + snu_ip + " 'mkdir " + path+"/"+SKtag +"/DATA/"+ s + "/"+ period+"'")

        endpath = path + "/"+SKtag +"/DATA/" + s +"/"+period
        status = -1
        while status == -1:
            status= makeTransferFile_snu(user_name,snu_ip,s,s_tag, endpath, file_user,SKtag+"_"+period)
            os.system("rm -r "+ s)
        if status == 10:
            print "#"*50
            print "All files transferred that can be, but some are still running on grid"
            print "#"*50
            rerun_samples.append(s_orig)
        if status == 0:
            print "#"*50
            print "Some jobs failed on grid. All successful jobs are transfered"
            print "#"*50
            complete_samples.append(s_orig)
        if status == 1:
            print "#"*50
            print "Job complete"
            print "#"*50
            complete_samples.append(s_orig)
        os.system("rm -r "+ s)


    n_runs=n_runs+1
