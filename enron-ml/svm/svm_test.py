from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# same few lines of code as naive bayes
X = [[0, 0], [1, 1]] #features
y = [0, 1]  #test
clf = SVC(kernel='linear')
clf.fit(X,y)
pred = clf.predict([[2., 2.]])
print(pred)
acc = accuracy_score(pred,[[2., 2.]] )
print(acc)
