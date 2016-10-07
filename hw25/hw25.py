from sklearn.neural_network import MLPClassifier
import csv
import numpy as np
import scipy
import matplotlib.pyplot as plt

def mt(x):
	return x * (1-x)

def gd(x):
	return 1/(1+np.exp(-x))

data0 = []
n=0.1
with open('hw25.csv', newline='') as csvfile:
	dataset = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in dataset:
		data0.append(row)
		# print(', '.join(row))

data = np.array(data0)
# print(data)
inset = np.delete(data,0,0)
inset = np.delete(inset,0,1)
# print(inset.size)

label = np.matrix(inset[:,0].astype(np.int)).T
attr0 = inset[:,range(1,7)].astype(np.int)
attr = np.hstack((attr0, np.ones((20,1),dtype=attr0.dtype)))
# weight = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1 ],dtype='float')
np.random.seed(1)
w0 = 2*np.random.random((7,4)) - 1
w1 = 2*np.random.random((5,1)) - 1
# print(label)
Error_list= []
for i in range(10000):
	L0 = attr
	L1 = gd(np.dot(L0,w0))
	L10 = np.hstack((L1, np.ones((20,1),dtype=attr0.dtype)))
	L2 = gd(np.dot(L10,w1))
	A = np.array(label)
	L2_error = A-L2

	Error = np.mean(np.abs(L2_error))
	Error_list.append(Error)
	L2_delta = L2_error * mt(L2)
	L1_error = L2_delta.dot(w1.T)
	L1_delta = mt(L10) * L1_error
	w1 += n*L10.T.dot(L2_delta)
	w0 += n*np.delete(L0.T.dot(L1_delta),-1,-1)
	if (i%10000==0):
		print(Error)
print(w0)
print(w1)
print(L2)
plt.plot(Error_list)
plt.show()
# clf = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(),max_iter=1000)
# print(clf.fit(attr, label))
# print(clf.predict(attr[range(0,20),:]))