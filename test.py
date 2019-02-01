import math
import statistics
a = [1,2,3]
modes = []
modes.append( max(set(a), key=a.count))
print(modes)
print( statistics.median(a))