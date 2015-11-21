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

# Reading commands in the file for each user 
with open(user_file) as f:
	content = f.readlines()
	content = [x.strip('\n') for x in content]

total_commands = content[0:5000]
distinct_commands = list(set(total_commands))
mat_len = len(distinct_commands)
mat_len_sq = mat_len*mat_len

sum = numpy.genfromtxt("output/user_" + user + ".csv", delimiter=",")
w, v = LA.eig(sum)

print w