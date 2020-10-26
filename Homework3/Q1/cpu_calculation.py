import time
import numpy as np

n = 3200
ni = np.int32(n) 

# matrix A 
a = np.random.randn(n, n)*10
a = a.astype(np.float32) 

# matrix B 
b = np.random.randn(n, n)*10
b = b.astype(np.float32)

# matrix B 
c = np.empty([n, n]) 
c = c.astype(np.float32)

# call gpu function
start = time.time()
for i in range(3):
    c = np.matmul(a, b)

end = time.time()
print ("CPU Time: %.5f s"%(end-start))
