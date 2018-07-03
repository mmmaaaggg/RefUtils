from sklearn import svm
import numpy as np
X = [[0, 0], [1, 1], [1, 0]]  # training samples   
y = [0, 1, 1]  # training target  
clf = svm.SVC()  # class   
clf.fit(X, y)  # training the svc model  
  
result = clf.predict(np.array([2, 2]).reshape((1,-1))) # predict the target of testing samples   
print(('result', result))  # target   
  
print(('clf.support_vectors_\n', clf.support_vectors_))  #support vectors  
  
print(('clf.support_', clf.support_))  # indeices of support vectors  
  
print(('clf.n_support_', clf.n_support_))  # number of support vectors for each class   