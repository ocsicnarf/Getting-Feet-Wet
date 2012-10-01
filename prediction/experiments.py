import time
import pylab as pl
import numpy as np
from sklearn import svm, neighbors, tree, linear_model, metrics
import datasets

start = time.time()

# load dataset
physio = datasets.load_physio_stats()
X = physio.data
y = physio.target
n_samples = X.shape[0]

# normalize features?
'''
X_mean = np.tile(X.mean(axis=0), (n_samples, 1))
X_std = np.tile(X.std(axis=0), (n_samples, 1))
X = (X - X_mean) / X_std
'''

# exclude the variance of each var
include = np.asarray(13 * range(5)) % 5 != 4
X = X[:, include]

# shuffle the samples
#np.random.seed(0)
order = np.random.permutation(n_samples)
X = X[order]
y = y[order].astype(np.float) # as float for the classifier?
split = 0.4 * n_samples

X_train = X[:split]
y_train = y[:split]
X_test = X[split:]
y_test = y[split:]

svm = svm.SVC(class_weight='auto', kernel='linear')
knn = neighbors.KNeighborsClassifier()
tree = tree.DecisionTreeClassifier()
logistic = linear_model.LogisticRegression(C=1e5)
classifiers = {'SVM': svm, 'Logistic': logistic,
               'Tree': tree, 'KNN': knn}

for name, c in classifiers.iteritems():
    print name, 'classifier:'
    c.fit(X_train, y_train)
    y_pred = c.predict(X_test)

    print 'Experiment took', time.time() - start, 'seconds'
    print metrics.classification_report(y_test, y_pred)
    print 'Confusion matrix:'
    print metrics.confusion_matrix(y_test, y_pred)
    print 'MCC:{0}'.format(metrics.matthews_corrcoef(y_test, y_pred))
    print
