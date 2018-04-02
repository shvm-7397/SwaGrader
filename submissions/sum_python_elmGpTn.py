import numpy as np 

a = np.random.randint(low=1, high=100000, size=1000000000, dtype='int64')
#print(a.shape[0])
for each in a :
	print(each, end = ' ')

# k sum constraints : n < 100000 and a[i] = 100000

