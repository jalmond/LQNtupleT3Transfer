def makeTransferFile_snu(snumachine, sample, endpath, username):
	import os
	
        #### not to change
	machine="uosaf0007.sscc.uos.ac.kr"
	path= "/cms/store/user/" +  username +"/Tag18/"
	dir=sample + "/"
	toremove = path+dir
    
        ###### DO COPY

	if not (os.path.exists(endpath)):
		os.system("mkdir " + endpath)
	if not (os.path.exists(endpath)):
		os.exit();

	if not (os.path.exists(sample)):
		os.system("mkdir " + sample)
		os.system("xrd " + machine + " ls " + path + dir + " > " + sample + "/" + sample +".txt")
	else:
		os.system("rm " + sample + "/*.txt")
		os.system("xrd " + machine + " ls " + path + dir + " > " + sample + "/" + sample +".txt")
		
	os.system("sed -i '/^$/d' " + sample +  "/" + sample +".txt")
	
	os.system("sed -r 's/^.{43}//' " + sample + "/" + sample + ".txt > " + sample + "/copy.txt")
	os.system("cut -d/ -f 8 " + sample + "/copy.txt > " + sample + "/fullsamplelist.txt")
	
        ## output the number of files from grid job
	
        ## check if rootfiles already exist in output location
	print "ssh jalmond@" + snumachine + ".snu.ac.kr 'cd "+ endpath  +"; ls  ./' > " + sample + "/remove_already_copiedfiles.txt"

	os.system("ssh jalmond@" + snumachine + ".snu.ac.kr 'cd "+ endpath  +"; ls  ./' > " + sample + "/remove_already_copiedfiles.txt")
	os.system("sed -i '/^$/d' " + sample + "/remove_already_copiedfiles.txt")
	
	fr = open(sample + '/remove_already_copiedfiles.txt' ,'r')
	for line in fr:
		if not "Agent pid " in line:
			print 'file ' + line.strip() + ' already copied, removing from list to be copied'  
		        # remove filename from copy.txt
			os.system("sed -i '/" + line.strip()+"/d' " + sample + "/copy.txt")
		
			print "removed all files previously copied"
		
	f = open(sample + '/copy.txt' ,'r')
	for line in f:
		# copy to local dir
		print 'copying '+ line.strip()
		copy = "xrdcopy root://" + machine+"/"
		fullpath = line.strip()
		os.system(copy+fullpath + " " + endpath + "/")  

		filename=line.strip()[len(toremove):]
		print "copied file removed from copy.txt"
		# remove filename from copy.txt
		os.system("sed -i '/" + filename+"/d' " + sample + "/copy.txt")
		
	print "Finished copying to " + snumachine + ".snu.ac.kr:/" + endpath + "."
	print "List of files copied are: "   
	os.system("ssh jalmond@" + snumachine + ".snu.ac.kr 'cd "+ endpath  +"; ls  ./'")
	os.system("ssh jalmond@" + snumachine + ".snu.ac.kr 'cd "+ endpath  +"; ls  ./' > " + sample + "/files_at_snuend.txt")

	
	os.system("grep -Fxv -f  " + sample + "/files_at_snuend.txt " + sample + "/fullsamplelist.txt > " + sample + "/missingfiles.txt")
	os.system("sed -i '/^$/d' " + sample + "/missingfiles.txt")
	
	fm = open(sample + '/missingfiles.txt' ,'r')
	for line in fm:
		# copy to local dir
		print 'File not copied originally is: '+ line.strip()  +". Retrying copy" 
		copy = "xrdcopy root://" + machine+"/"
		fullpath = line.strip()
		os.system(copy+fullpath + " " + endpath + "/")
    
		filename=line.strip()[len(toremove):]
		# remove filename from copy.txt
		os.system("sed -i '/" + filename+"/d' " + sample + "/missingfiles.txt")
                                                    
	print "Doing final check. Files failed to copy ="
	os.system("ssh jalmond@" + snumachine + ".snu.ac.kr 'cd "+ endpath  +"; ls  ./' > " + sample + "/files_at_snuend_v2.txt")

	os.system("grep -Fxv -f  " + sample + "/files_at_snuend_v2.txt " + sample + "/fullsamplelist.txt")

	os.system("rm " + sample + "/*.txt")	

def rename(snumachine, sample, endpath):
	import os
	rename=True
	if rename:
		os.system("ssh jalmond@" + snumachine + ".snu.ac.kr 'cd "+ endpath  +"; ls  ./' > " + sample + "/copiedfiles.txt")
		fr = open(sample + '/copiedfiles.txt' ,'r')
		for line in fr:
			newline=line.replace("rootTupleMaker_CRAB_MC_2012_Top","rootTupleMaker_CRAB_MC_2012_" + sample)
			os.system("mv  " + endpath + "/" + line[:-1] + " " + endpath + "/" + newline[:-1])


