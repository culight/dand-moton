from sklearn.tree import DecisionTreeClassifier

X = [[0,0], [1,1]]
Y = [0,1]

clf = DecisionTreeClassifier()
clf = clf.fit(X, Y)
pred = clf.predict([[2., 2.]])

print(pred)
