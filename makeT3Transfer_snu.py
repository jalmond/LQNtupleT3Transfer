def makeTransferFile_snu(snumachine, sample, endpath, username, pub_name):
	import os
	ranpath=""
	data=0
	
	data_stream=""
	if "DoubleElectron" in sample:
		data_stream="DoubleElectron"
	if "DoubleMu" in sample:
		data_stream="DoubleMuon"
	if "SingleMu" in sample:
		data_stream="SingleMu"
 	if "SingleElectron" in sample:
		data_stream="SingleElectron"
	if "MuEG" in sample:
		data_stream="ElectronMuon"

	fileA=data_stream+"periodA.txt"
	fileB=data_stream+"periodB.txt"
	fileC=data_stream+"periodC.txt"
	fileD=data_stream+"periodD.txt"
	endpath1=""
	endpath2=""

	if not (os.path.exists(fileA)):
		 print "File " + fileA + " does not exist. Please copy to current directory"
		 os.exit()
	if "DoubleElectron" in endpath:
		endpath1 = "/data1/DATA/LQNtuples_5_3_14_snu27/Data/DoubleElectron/"
	elif "DoubleMu" in endpath:
		endpath1 = "/data1/DATA/LQNtuples_5_3_14_snu27/Data/DoubleMuon/"
	elif "SingleElectron" in endpath:
		endpath1 = "/data1/DATA/LQNtuples_5_3_14_snu27/Data/SingleElectron/"
	elif "SingleMuon" in endpath:
		endpath1 = "/data1/DATA/LQNtuples_5_3_14_snu27/Data/SingleMuon/"
	elif "ElectronMuon" in endpath:
		endpath1 = "/data1/DATA/LQNtuples_5_3_14_snu27/Data/ElectronMuon/"
	

	if "data" in pub_name:
		data=1
			

        #### not to change
	machine="uosaf0007.sscc.uos.ac.kr"
	if not (os.path.exists(sample)):
		os.system("mkdir " + sample)
		
	os.system("xrd " + machine + " ls /cms/store/user/" +  username +"/" + sample + "/" + pub_name +"/" + " > " + sample + "/getranpath.txt")
	print "xrd " + machine + " ls /cms/store/user/" +  username +"/" + sample + "/" + pub_name +"/" + " > " + sample + "/getranpath.txt"
	
	os.system("sed -i '/^$/d' " + sample +  "/getranpath.txt")
	os.system("sed -r 's/^.{43}//' " + sample + "/getranpath.txt  > " + sample + "/getranpath_skim.txt")	
	os.system("cut -d/ -f 8 " + sample + "/getranpath_skim.txt > " + sample + "/ranpath.txt")
	
	
	frp = open(sample + '/ranpath.txt' ,'r')	
	iline=0
	for linerp in frp:
		if iline < 1:
			ranpath = linerp.strip()
			print "ranpath = " + linerp.strip()
			iline= iline+1


	path= "/cms/store/user/" +  username +"/" + sample + "/" + pub_name +"/" + str(ranpath) + "/"
	dir=sample + "/"
	toremove = path
	
	print ""
	print "###############################################################################"
	print "###"
	print "### STARTING NEW TRANSFER OF SAMPLE    " + sample
	print "###"
	print "################################################################################"
	print ""
        ###### DO COPY
	print "Setting up transfer"
	if not (os.path.exists(endpath)):
		os.system("mkdir " + endpath)
	if not (os.path.exists(endpath)):
		os.exit();
	if data == 1:
		if not (os.path.exists(endpath1)):
			os.system("mkdir " + endpath1)
		if not (os.path.exists(endpath1+ "/periodA")):
			os.system("mkdir " + endpath1 + "/periodA")
		if not (os.path.exists(endpath1+ "/periodB")):
			os.system("mkdir " + endpath1 + "/periodB")
		if not (os.path.exists(endpath1+ "/periodC")):
			os.system("mkdir " + endpath1 + "/periodC")
		if not (os.path.exists(endpath1+ "/periodD")):
                       os.system("mkdir " + endpath1 + "/periodD")	

	if not (os.path.exists(sample)):
		os.system("mkdir " + sample)
		print "xrd " + machine + " ls " + path + " > " + sample + "/" + sample +".txt"
		os.system("xrd " + machine + " ls " + path + " > " + sample + "/" + sample +".txt")
	else:
		os.system("rm " + sample + "/*.txt")
		print "xrd " + machine + " ls " + path  + " > " + sample + "/" + sample +".txt"
		os.system("xrd " + machine + " ls " + path  + " > " + sample + "/" + sample +".txt")

	os.system("sed -i '/^$/d' " + sample +  "/" + sample +".txt")
	
	os.system("sed -r 's/^.{43}//' " + sample + "/" + sample + ".txt > " + sample + "/copy.txt")
	os.system("cut -d/ -f 9 " + sample + "/copy.txt > " + sample + "/fullsamplelist.txt")
	
        ## output the number of files from grid job
	
        ## check if rootfiles already exist in output location
	print "ssh jalmond@" + snumachine + ".snu.ac.kr 'cd "+ endpath  +"; ls  ./' > " + sample + "/remove_already_copiedfiles.txt"

	os.system("ssh jalmond@" + snumachine + ".snu.ac.kr 'cd "+ endpath  +"; ls  ./' > " + sample + "/remove_already_copiedfiles.txt")
	os.system("sed -i '/^$/d' " + sample + "/remove_already_copiedfiles.txt")

	print "Removing files already copied"
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
	os.system("ssh jalmond@" + snumachine + ".snu.ac.kr 'cd "+ endpath  +"; ls  ./' > " + sample + "/files_at_snuend.txt")
	
	fatsnu = open(sample + '/files_at_snuend.txt')
	for line in fatsnu:
		if not "Agent pid " in line:		
			print line
			
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

	
	if not "MC" in endpath:
		dir = endpath
		tocheck = "rootTupleMaker_CRAB_DATA_2012_53X_"
		print "Number of files in directory = "
		count = os.system("ls -1 " + str(dir) + "  | wc -l")
		os.system("cd " + str(dir) );
		os.system("ls " + str(dir) + "/*.root > "+ sample+ "/duplcheck.txt")
		isfile = os.path.isfile
		join = os.path.join
		number_of_files = sum(1 for item in os.listdir(dir) if isfile(join(dir, item)))

		print "Checking for duplicated Job ID :" + tocheck + "[jobid]" + "_##.root"

		
		count = number_of_files
		dupl =0
		fr = open(sample + '/duplcheck.txt','r')
		for line in fr:
			print "line = " + line
			frA = open(fileA,'r')
			frB = open(fileB,'r')
			frC = open(fileC,'r')
			frD = open(fileD,'r')
			found_file=0
			for lineA in frA:
				if lineA in line:
					endpath2 = endpath1 + "/periodA/"
					found_file=1
       			for lineB in frB:  
				if lineB in line:
					endpath2 = endpath1 + "/periodB/"
					found_file=1		      	
			for lineC in frC:   		
				if lineC in line:
					endpath2 = endpath1 + "/periodC/"
					found_file=1
			for lineD in frD: 
				if lineD in line:
					endpath2 = endpath1 + "/periodD/"
					found_file=1

			if found_file==1:
				print "mv " + line.strip() + " " + endpath2
				os.system("mv " + line.strip() + " " + endpath2)
		       	if found_file==0:
				print "File NOT found"
				print "Will remove: " + line 
				os.system("rm " + line)
				ft3 = open(sample+'/fullsamplelist.txt' ,'r')	
				for t3line in ft3:
					# copy to local dir
					if "rootTupleMaker_CRAB_DATA" in t3line:
						if t3line in line:
							clean = "xrd " + machine + " rm "
							fullpatht3 = path  + "/" + t3line
							print "File will be removed from tier3: "  + fullpatht3
							os.system(clean+fullpatht3)
							print "Removing file " + fullpatht3 + " from tier3" 
							
	        if dupl == 0:
			print "No duplicated jobs in directory"

		print "Number of files in directory after check = "
		count = os.system("ls -1 " + str(dir) + "  | wc -l")
		
	else:
		dir = endpath
		tocheck = "file_"
		print "Number of files in directory = "
		count = os.system("ls -1 " + str(dir) + "  | wc -l")
		os.system("cd " + str(dir) );
		os.system("ls " + str(dir) + "/*.root > " + sample+"/duplcheck.txt")
		isfile = os.path.isfile
		join = os.path.join
		number_of_files = sum(1 for item in os.listdir(dir) if isfile(join(dir, item)))
		
		print "Checking for duplicated Job ID :" + tocheck + "[jobid]" + "_##.root"
		
		count = number_of_files
		dupl =0
		for i in range(1, count):
			fullname = tocheck + str(i) + "_"
			nrepeat=0
			fr = open(sample + '/duplcheck.txt','r')
			for line in fr:
				if fullname in line:
					nrepeat+=1
					print "Job " + str(i)  + ": --> " +  line
					if nrepeat != 1:
						print "FOUND TWICE: removing " + line
						os.system("rm " + line)
						dupl+=1
						### remove duplicate on tier3
						#os.system("xrd " + machine + " ls " + path + sample + "/" + " > " + sample + "/dupl" + sample +".txt")
						#os.system("sed -r 's/^.{43}//' " + sample + "/dupl" + sample + ".txt > " + sample + "/duplclean.txt")
						#os.system("cut -d/ -f 9 " + sample + "/duplclean.txt > " + sample + "/duplfullsample.txt")
						ft3 = open(sample+'/fullsamplelist.txt' ,'r')
						for t3line in ft3:
							if "file" in t3line:
								# copy to local dir
								if t3line in line:
									clean = "xrd " + machine + " rm "
									fullpatht3 = path  + "/" + t3line
									os.system(clean+fullpatht3)
									print "Removing file " + fullpatht3 + " from tier3"
      	     	if dupl == 0:
			print "No duplicated jobs in directory"
		print "Number of files in directory after check = "
		count = os.system("ls -1 " + str(dir) + "  | wc -l")

		print "Making list for Ferdinando"
		os.system("xrd " + machine + " ls " + path  + " > " + sample + "/fg" + sample +".txt")
		os.system("sed -i '/^$/d' " + sample +  "/fg" + sample +".txt")
		os.system("sed -r 's/^.{43}//' " + sample + "/fg" + sample + ".txt > " + sample + "/fgcopy.txt")

		
		output_fg = open("/home/jalmond/GridList/"+sample + "_snu27.txt" ,"w")
		fg = open(sample + '/fgcopy.txt' ,'r')
		for line in fg:
			# copy to local dir
			copy = "root://" + machine+"/"
			fullpath = line.strip()
			output_fg.write(copy+fullpath + "\n")
	       	output_fg.close()
																								
																								
def rename(snumachine, sample, endpath):
	import os
	rename=True
	if rename:
		os.system("ssh jalmond@" + snumachine + ".snu.ac.kr 'cd "+ endpath  +"; ls  ./' > " + sample + "/copiedfiles.txt")
		fr = open(sample + '/copiedfiles.txt' ,'r')
		for line in fr:
			newline=line.replace("rootTupleMaker_CRAB_MC_2012_Top","rootTupleMaker_CRAB_MC_2012_" + sample)
			os.system("mv  " + endpath + "/" + line[:-1] + " " + endpath + "/" + newline[:-1])


