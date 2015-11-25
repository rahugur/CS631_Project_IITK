#!/usr/bin/python
# since the sizes of the matrices are different	
# creating the co-occurence matrix for each user.

# Enter the userid and userfilename as command line argument
import sys
import numpy
from numpy import linalg as LA
user = sys.argv[1]

print "done 3"
sum = numpy.genfromtxt("output/user_" + user + ".csv", delimiter=",")
w, v = LA.eigh(sum)

numpy.savetxt("output/user_eigenvalues_" + user + ".csv", w, delimiter=",")

