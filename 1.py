#!/usr/bin/python 
# creating the co-occurence matrix for each user.
win_size = 5
for user in range(1, 51):
	user_file = 'hw1/User' + str(user)

	# Reading commands in the file for each user 
	with open(user_file) as f:
		content = f.readlines()
		content = [x.strip('\n') for x in content]
	
	for j in range(0, 50):							# Making slots of 100 commadns for each user
		commands = content[(j)*100: (j+1)*100]
		commands_unique = list(set(commands))				# Removing duplicates fromt he c
		co_mat = []											# Co occurence matrix, list of lists
		for command in commands_unique:
			temp_row = [0]*len(commands_unique)									# Each row of the cooccurence matrix
			for k in range(0, 100):
				if(commands[k] == command):
					for l in range(1, win_size):
						if((l+k)>99):
							break
						comm = commands[l+k]
						ind = commands_unique.index(comm)
						temp_row[ind] += 1

			co_mat.append(temp_row)
		# print co_mat
		# print '\n\n\n\n\n\n\n\n\n\n\n\n\n'

# To be done later ------------

# m is the 
# n is the 

