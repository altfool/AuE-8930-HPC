import numpy as np
b = np.arange(1, 21).reshape([4, 5])
a = np.random.randint(-2, 2, [4, 5])
print("a is: \n{}\nb is: \n{}".format(a, b))
print("a + b is: \n{}".format(a+b))
print("a - b is: \n{}".format(a-b))
print("a * b is: \n{}".format(a*b))
print("a / b is: \n{}".format(a/b))
