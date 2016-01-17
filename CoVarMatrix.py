#!/usr/bin/python
# since the sizes of the matrices are different	
# creating the co-occurence matrix for each user.

# Enter the userid and userfilename as command line argument
import sys
import numpy
user = sys.argv[1]
user_file = 'hw1/User' + str(user)
mapping_mat = []
win_size = 5

def mat_create(size):
	matricx = []
	for i in range(size):
		a = [0]*size
		matricx.append(a)
	return matricx

# Reading commands in the file for each user 
with open(user_file) as f:
	content = f.readlines()
	content = [x.strip('\n') for x in content]

total_commands = content[0:5000]
distinct_commands = list(set(total_commands))
mat_len = len(distinct_commands)
total_mat = mat_create(mat_len)
count_mat = mat_create(mat_len)
avg_mat = mat_create(mat_len)
comat_log = []									# List of co occurence matrices for all spaces of the current user
for j in range(0, 50):							# Making slots of 100 commadns for each user
	commands = content[(j)*100: (j+1)*100]
	commands_unique = list(set(commands))				# Removing duplicates fromt he c
	mapping_mat.append(commands_unique)					# Appending the unique commands list to the mapping matrix
	co_mat = []											# Co occurence matrix, list of lists
	for command in distinct_commands:
		temp_row = [0]*len(distinct_commands)									# Each row of the cooccurence matrix
		for k in range(0, 100):
			if(commands[k] == command):
				for l in range(1, win_size):
					if((l+k)>99):
						break
					comm = commands[l+k]
					ind = distinct_commands.index(comm)
					temp_row[ind] += 1
		try:
			for k in range(len(temp_row)):
				if(temp_row[k]):
					ind_i = distinct_commands.index(command)
					total_mat[ind_i][k] += temp_row[k]
					count_mat[ind_i][k] += 1
		except:
			 e = sys.exc_info()[0]
		co_mat.append(temp_row)
	comat_log.append(co_mat)

# Computing the average (biggest size) matrix
for i in range(mat_len):
	for j in range(mat_len):
		if(count_mat[i][j]==0):
			avg_mat[i][j] = 0
		else:
			avg_mat[i][j] = float(total_mat[i][j])/count_mat[i][j]

for i in range(50):
	for j in range(len(distinct_commands)):
		for k in range(len(distinct_commands)):
			comat_log[i][j][k] -= avg_mat[j][k]

mat_len_sq = mat_len*mat_len
sum = numpy.zeros(shape=(mat_len_sq, mat_len_sq))
for i in range(50):
	# print i
	flattened = [val for sublist in comat_log[i] for val in sublist]
	# print flattened
	# Calculating F[T]*F
	temp = []
	for j in range(mat_len*mat_len):
		temp_1 = []
		for k in range(mat_len*mat_len):
			temp_1.append(flattened[j]*flattened[k])
		temp.append(temp_1)
	for j in range(mat_len_sq):
		for k in range(mat_len_sq):
			sum[j][k] += temp[j][k]
			
numpy.savetxt("output/user_" + user + ".csv", sum, delimiter=",")
