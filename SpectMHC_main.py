import SpectMHC_methods
import glob, os
import threading
import itertools


def add_thread(r, path,version, out_list,threads_list, threads_list_process):
		head, sep, tail = r[2].partition('.f')
		print('\nfile %s is executed' %head)
		outfile='%s_%d_%s_output.txt' %(head, r[0],r[1])
		out_list.append(outfile)
		if version in '4.0':
			command = '%s/netMHC -l %d -a %s %s > %s' %(path, r[0], r[1], r[2], outfile)
		elif version in 'pan':
			command = '%s/netMHCpan -l %d -a %s %s > %s' %(path, r[0], r[1], r[2], outfile)			
		elif version in '3.4':
			command = '%s/netMHC -l %d -a %s %s > %s' %(path, r[0], r[1], r[2], outfile)
		threads_list.append(threading.Thread(target = SpectMHC_methods.executeos , args=(command,)))

def main():
	path = "/home/lab/Desktop/netMHCpan-4.1"
	num = "8 9 10 11 12"
	input_list = num.split()
	input_list = [int(a) for a in input_list]
	all_input = "HLA-A0210 HLA-A6801 HLA-B3503 HLA-C0401 HLA-C0701 HLA-B3901"
	alleles_list = all_input.split()
	out_list = []
	threads_list= []
	threads_list_process= []
	#split_list = SpectMHC_methods.split_files("split")
	list_of_files = ['data_3_1_2022.fasta']
	data_to_be_processesed = itertools.product(input_list,alleles_list,list_of_files)
	print(data_to_be_processesed)
	version = SpectMHC_methods.version("verify version")
	for r in data_to_be_processesed :
		add_thread(r, path,version, out_list,threads_list, threads_list_process)
	### create threads
	if SpectMHC_methods.install_check("verify") in 'yes':
		print ("\nOk, Let's move ahead")
		version = SpectMHC_methods.version("verify version")
		split_output='yes'
		if split_output in 'yes':
			check1 = 'yes'#hard coded save to file
			check2 = 'yes'# hard coded output in fasta format
			if check2 in 'yes':
				# A thread should run here 
				for x in threads_list:
					x.start()
				for x in threads_list:
					x.join()
				print ("\nWait while your data is processed into fasta format...")
				if check2 in 'yes':
					# a thread should run here 
					map(lambda x : x.start(),threads_list_process)
					map(lambda x : x.join(),threads_list_process)
					print("\nnetMHC execution completed ...only raw")
	
if __name__ == "__main__":
	main()
