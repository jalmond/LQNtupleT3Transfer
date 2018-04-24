def makeTransferFile_snu(snuuser,snumachine, sample,sample_tag, endpath, username, pub_name):
	import os,sys

	import ROOT

	ranpath=""
	data=0
	
        #### not to change
	if not (os.path.exists(sample)):
		os.system("mkdir " + sample)
	else:
		os.system("rm -rf " + sample + "/*")

	os.system("ls /xrootd/store/user/" +  username +"/SKFlat/" + sample + "/" + pub_name +"/" + " > " + sample + "/getranpath.txt")
	print "ls /xrootd/store/user/" +  username +"/SKFlat/" + sample + "/" + pub_name +"/" + " > " + sample + "/getranpath.txt"
	
	os.system("sed -i '/^$/d' " + sample +  "/getranpath.txt")
	os.system("sed -r 's/^.{43}//' " + sample + "/getranpath.txt  > " + sample + "/getranpath_skim.txt")	
	os.system("cut -d/ -f 8 " + sample + "/getranpath_skim.txt > " + sample + "/ranpath.txt")

	
	frp = open(sample + '/ranpath.txt' ,'r')	
	iline=0
	for linerp in frp:
		ranpath = linerp.strip()
		print "ranpath = " + linerp.strip()
		iline= iline+1
		

	if not sample_tag == "":
		ranpath= sample_tag
		print "Setting path by hand"

	dir=sample + "/"
	path= "/xrootd/store/user/" +  username +"/SKFlat/" + sample + "/" + pub_name +"/" + str(ranpath) + "0000/" 
	toremove = path
	
	RetryCounter=True
	retries=0
	while RetryCounter:
		if os.path.exists("/xrootd/store/user/"+username+"/SKFlat/" + sample + "/" + pub_name +"/" + str(ranpath) + "/000" + str(retries)+"/"):
			print "/xrootd/store/user/"+username+"/SKFlat/" + sample + "/" + pub_name +"/" + str(ranpath) + "/000" + str(retries)+"/"
			retries+=1
		else:
			RetryCounter=False


        print 			"Total number of retries = " + str(retries)

	print ""
	print "###############################################################################"
	print "###"
	print "### STARTING NEW TRANSFER OF SAMPLE    " + sample
	print "###"
	print "################################################################################"
	print ""
        ###### DO COPY
	print "Setting up transfer"

	for x in range(0,retries):
		addto = " >> "
		if x == 0:
			addto =" > "
		
		path= "/xrootd/store/user/" +  username +"/SKFlat/" + sample + "/" + pub_name +"/" + str(ranpath) + "/000" + str(x)+ "/"
		
		if not (os.path.exists(sample)):
			os.system("mkdir " + sample)
			print "ls " + path + "* " + addto + sample + "/" + sample +".txt"
			os.system("ls " + path + "* "+ addto + sample + "/" + sample +".txt")
		else:
			print "ls " + path  + "* " +  addto + sample + "/" + sample +".txt"
			os.system("ls " + path  + "* " + addto + sample + "/" + sample +".txt")

	os.system("sed -i '/^$/d' " + sample +  "/" + sample +".txt")
	
	
	remove_log = open(sample + "/"+sample +".txt", "r")

	#os.system("sed -r 's/^.{0}//' " + sample + "/" + sample + ".txt > " + sample + "/copy.txt")
	copy_log = open(sample + "/copy.txt", "w")

	incomplete_files=[]
	failed_files=[]
	for line in  remove_log:
		s=line.split()
		s=s[0]

		if ".root" in line:
			if not "/xrootd" in line:
				failed_files.append(s)
				continue
			f = ROOT.TFile(s)
			if f.IsZombie() :
				print "Error " + line
				incomplete_files.append(s)
			elif not f:
				print "Error " + line
				incomplete_files.append(s)

			elif f.TestBit(ROOT.TFile.kRecovered):
				incomplete_files.append(s)
			else:
				copy_log.write(line)
	copy_log.close()
	print "_"*50

	print "File not copied, as crab transfer incomplete are:"
	print "_"*50
	for s in incomplete_files:
		print s
	print "_"*50
	print "File not copied, as failed in crab are:"
	print "_"*50
	for s in failed_files:
		print s

	remove_log.close()


        ## output the number of files from grid job
	
        ## check if rootfiles already exist in output location
	print "ssh "+snuuser+"@" + snumachine + " 'cd "+ endpath  +"; ls  ./' > " + sample + "/remove_already_copiedfiles.txt"

        os.system("ssh "+snuuser+"@" + snumachine + " 'mkdir " + endpath + "'")
	os.system("ssh "+snuuser+"@" + snumachine + " 'cd "+ endpath  +"; ls  ./' > " + sample + "/remove_already_copiedfiles.txt")
	os.system("sed -i '/^$/d' " + sample + "/remove_already_copiedfiles.txt")

	print "Removing files  already copied to SNU from list to copy:"
	fr = open(sample + '/remove_already_copiedfiles.txt' ,'r')
	for line in fr:
		if not "Agent pid " in line:
			#print 'file ' + line.strip() + ' already copied, removing from list to be copied'  
		        # remove filename from copy.txt
			FixList(line.strip(), sample)
			
       	print "removed all files previously copied........"
		
	f = open(sample + '/copy.txt' ,'r')
	
	for line in f:
		job_tag=""
		if not "Error" in line:
			if not "child" in line:
				if ".root" in line:
					# copy to local dir
					print line
					line2=line.replace("/"," ")
					sline = line2.split()
					new_filename=""
					for s in sline:
						if ".root" in s:
							new_filename=s.replace(".root","_"+job_tag+".root")
						job_tag=s
					splitline=line.split()
					print "scp " + splitline[0] +  "  " + snuuser + "@" + snumachine +":" + endpath + "/"+new_filename
					os.system("scp " + splitline[0] +  "  " + snuuser + "@" + snumachine +":" + endpath + "/"+new_filename)
				elif "failed" in line:
					filename=line.strip()[len(toremove):]
                                        os.system("sed -i '/" + filename+"/d' " + sample + "/copy.txt")
					
					

	os.system("ssh " + snuuser + "@" + snumachine +  " 'root -l -q -b  "+ endpath + "' >   " + sample + "/corruptfiles.txt")
	Failed_copy= DeleteCorruptFiles(sample + "/corruptfiles.txt")
	

	print "List of files successfully copied to SNU are: "   
	os.system("ssh "+snuuser+"@" + snumachine + " 'cd "+ endpath  +"; ls  ./' > " + sample + "/files_at_snuend.txt")
	
	# status 1 means all finished and copied
	job_status=1

	if failed_files > 0:
		# status 10 means that all copied but some failed in crab
		job_status=10

	if incomplete_files > 0:
		# status 0 means that all files are copied to SNU but some are still transferring from crab
		job_status=0
	if Failed_copy > 0:
		# status -1 means some failed to copy that can be copied
		job_status = -1
	
	if job_status==1:
		print  "Successful job: Number of rootfiles in " + endpath +" is: " 
		os.system("ssh "+snuuser+"@" + snumachine + " 'cd "+ endpath  +"; ls -1 | wc -l'")
	else:
		print   "Non complete:  Number of rootfiles in " + endpath +" is: "
                os.system("ssh "+snuuser+"@" + snumachine + " 'cd "+ endpath  +"; ls -1 | wc -l'")

	return job_status


def rename(snumachine, sample, endpath):
	import os
	rename=True
	if rename:
		os.system("ssh jalmond@" + snumachine + ".snu.ac.kr 'cd "+ endpath  +"; ls  ./' > " + sample + "/copiedfiles.txt")
		fr = open(sample + '/copiedfiles.txt' ,'r')
		for line in fr:
			newline=line.replace("rootTupleMaker_CRAB_MC_2012_Top","rootTupleMaker_CRAB_MC_2012_" + sample)
			os.system("mv  " + endpath + "/" + line[:-1] + " " + endpath + "/" + newline[:-1])




def FixList(remove_line,sample):
	import os
	
	remove_line1=remove_line[:-10]+".root"
	remove_line2=remove_line[len(remove_line)-9:-5]
	remove_line2="/"+remove_line2+"/"

	list_log = open(sample + "/copy.txt", "r")
        copy_log = open(sample + "/copy2.txt", "w")

        for line in  list_log:
		if remove_line1 in line and remove_line2 in line:
			print "Removing " + line
		else:
			copy_log.write(line)
        copy_log.close()
	list_log.close()
	os.system("cp  " + sample + "/copy2.txt  " + sample + "/copy.txt")
	os.system("rm " + sample + "/copy2.txt")


def DeleteCorruptFiles(path):
	import os
	list_corrupt = open(path  ,"r")
	nfiles_corr=0

	for line in list_corrupt:
		if "Error in <TFile::Init>:" in line:
			sline =  line.split()
			filepath_corr= sline[4]
			os.system("ssh " + snuuser + "@" + snumachine +  " 'rm "+ filepath_corr +"'")
			print "Deleted " + filepath_corr + " as the copy failed"
			nfiles_corr=nfiles_corr+1
	list_corrupt.close()

	return nfiles_corr


def CheckSetup(username_k, snu_ip):

	import os
	root_v=os.getenv("ROOTSYS")
	cmssw_v=os.getenv("CMSSW_VERSION")
	if root_v == "":
		print "Setup CMSSW or root and rerun"
		quit()

	os.system("cat ~/.ssh/config > check_connection.txt")
	ch_connect = open("check_connection.txt",'r')
	cpath="/tmp/"
	for line in ch_connect:
		if "ControlPath" in line:
			if "~/ssh" in line:
				cpath="~/"
			elif "/tmp/" in line:
				cpath="/tmp/"
			else:
				print "Modify the cms21 connection since  ControlPath in ~/.ssh/cofig is set to something other than tmp or home dir"
				
	os.system("ls " + cpath + " > check_snu_connection.txt")
	snu_connect = open("check_snu_connection.txt",'r')
	connected_cms3=False
	connected_cluster=False
	for line in snu_connect:
		if "ssh-"+username_k+"@"+snu_ip in line:
			connected_cms3=True
	os.system("rm check_snu_connection.txt")
	if connected_cms3 == False:
		print "No connection to cms3: please make connection in screen and run script again"
		quit()
