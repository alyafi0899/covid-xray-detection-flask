import numpy as np

data = np.array([5,5,5,5,8,7,7,7,8,7,7,7,8,8,8,10,8,10,10,50,10,15,15,15,15,15,100,25,10,25,15])
data_actual = np.array([5,7,7,7,8,7,7,7,8,8,8,10,8])

print(data)
print(data.mean())
print(data.std())
print(data.sum())

print("\n", (data.mean())+(data.std()))
print("\n", (data.mean())-(data.std()))


print(data_actual)
print(data_actual.mean())
print(data_actual.std())
print(data_actual.sum())

print("\n", (data_actual.mean())+(data_actual.std()))
print( (data_actual.mean())-(data_actual.std()))

print("\n", (data_actual.sum())-(data_actual.max()))
print( (data_actual.max()))