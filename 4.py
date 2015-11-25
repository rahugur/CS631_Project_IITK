#!/usr/bin/python
# since the sizes of the matrices are different	
# creating the co-occurence matrix for each user.

# Enter the userid and userfilename as command line argument
import sys
import numpy
from numpy import linalg as LA
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

print "done 1"
total_commands = content[0:5000]
distinct_commands = list(set(total_commands))
mat_len = len(distinct_commands)
mat_len_sq = mat_len*mat_len
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

print "done 2"
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

print "done 3"
sum = numpy.genfromtxt("output/user_" + user + ".csv", delimiter=",")
w, v = LA.eigh(sum)
#v_list = v.tolist()
print "done 4"
#c = lambda x: w[v_list.index(x)]
#newlist = sorted(w, key=c, reverse=False)
#Converting to list for sorting 
X = v.tolist()
Y = w.tolist()

newlist = [x for (y,x) in sorted(zip(Y,X))]

sum = 0
breaking_i = 50
POSH = 0
#h
eigen_coucc_mat = numpy.zeros(shape=(breaking_i))

print "done 5"
for k in range(breaking_i):
	cooc = numpy.zeros(shape=(mat_len,mat_len))
	for i in range(mat_len):
		for j in range(mat_len):
			cooc[i][j] = newlist[k][i*mat_len+j]
	eigen_coucc_mat.append(cooc)

allpos_layer = numpy.zeros(shape=50)
for l in range(50):
	pos_layer = numpy.zeros(shape=breaking_i)
	for k in range(breaking_i):
		a_cap = numpy.zeros(shape=mat_len_sq)
		poslay = numpy.zeros(shape=(mat_len,mat_len))
		for i in range(mat_len):
			for j in range(mat_len):
				a_cap[i*mat_len + j] = comat_log[l][i][j]
		m = 0
		for i in range(mat_len_sq):
			m += a_cap[i]*newlist[k][i]
		# matrix sum fi*Vi
		for i in range(mat_len):
			for j in range(mat_len):
				const = eigen_coucc_mat[k][i][j]*m
				if (const>POSH):
					poslay[i][j] = 1
		pos_layer.append(poslay)
	allpos_layer.append(pos_layer)

print "done 6"
numpy.savetxt("output/user_fv_" + user + ".csv", sum, delimiter=",")

test_comat = []
for j in range(50,150):
	commands = content[(j)*100: (j+1)*100]
	commands_unique = list(set(commands))
	co_mat = []
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
		co_mat.append(temp_row)
	test_comat.append(co_mat)
for i in range(100):
	for j in range(len(distinct_commands)):
		for k in range(len(distinct_commands)):
			test_comat[i][j][k] -= avg_mat[j][k]

max_sim_mat = []
for i in range(100):
	pos_layer = numpy.zeros(shape=breaking_i)
	for k in range(breaking_i):
		a_cap = numpy.zeros(shape=mat_len_sq)
		poslay = numpy.zeros(shape=(mat_len,mat_len))
		for m in range(mat_len):
			for j in range(mat_len):
				a_cap[m*mat_len + j] = test_comat[i][m][j]
		fv_point = 0
		for m in range(mat_len_sq):
			fv_point += a_cap[m]*newlist[k][m]
		for m in range(mat_len):
			for j in range(mat_len):
				const = eigen_coucc_mat[k][m][j]*m
				if (const>POSH):
					poslay[i][j] = 1
		pos_layer.append(poslay)
	#Only similarity checking left
	max_similarity = 0
	for j in range(50):
		similarity = 0
		for k in range(breaking_i):
			for a in range(mat_len):
				for b in range(mat_len):
					for c in range(mat_len):
						if (a-b)*(b-c)*(c-a)!=0:
							temp_add = allpos_layer[j][k][a][b]*allpos_layer[j][k][b][c]*pos_layer[k][a][b]*pos_layer[k][b][c]
							similarity += temp_add
		if similarity>max_similarity:
			max_similarity=similarity
			
	max_sim_mat.append(max_similarity)
# Computing the min amd max of the similarity list of sequences for a user
max_sim = max(max_sim_mat)
min_sim = min(max_sim_mat)

# Parsing the reference.txt 
f = open('hw1/reference.txt', 'rb');
a = f.readlines()
a = [x.strip() for x in a]
corr_classified = []
for i in a:
	corr_classified.append(i.split()[user-1])

const = float(max_sim - min_sim)/100
detection = numpy.zeros(shape=(100, 2))
for i in range(100):
	epsilon = min_sim + i*const
	test_classified = []
	for j in range(100):
		if max_sim_mat[j]>epsilon:
			test_classified.append(1)
		else:
			test_classified.append(0)
	# Matching the results with correct given data 
	correct_detection = 0
	false_detection = 0
	for j in range(100):
		if test_classified[j]*corr_classified[j] == 1:
			correct_detection += 1
		if test_classified[j] == 1 and corr_classified[j] == 0:
			false_detection += 1
	detection[i][0] = correction_detection
	detection[i][1] = false_detection

numpy.savetxt("output/user_graph_" + user + ".csv", detection, delimiter=",")
