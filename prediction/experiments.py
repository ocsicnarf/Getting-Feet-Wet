import time
import pylab as pl
import numpy as np
from sklearn import svm, neighbors, tree, linear_model, metrics
from sklearn import ensemble
from sklearn import cross_validation
import datasets
import decorators

def _compare_classifiers(classifiers):
    # load dataset
    physio = datasets.load_physio_stats()
    X = physio.data
    y = physio.target
    n_samples = X.shape[0]

    # normalize features (SVM classifier train
    X_mean = np.tile(X.mean(axis=0), (n_samples, 1))
    X_std = np.tile(X.std(axis=0), (n_samples, 1))
    X = (X - X_mean) / X_std
    
    # exclude the variance of each var
    include = np.asarray(13 * range(5)) % 5 != 4
    X = X[:, include]

    # construct training and testing sets
    X_train, X_test, y_train, y_test =\
        cross_validation.train_test_split(X, y, test_size = 0.75)

    for name, c in classifiers.iteritems():
        print '--- {0} Classifier ---'.format(name)
        start = time.time()
        c.fit(X_train, y_train)
        y_pred = c.predict(X_test)

        print 'Training and testing took', time.time() - start, 'seconds'
        print metrics.classification_report(y_test, y_pred)
        print
        print 'Confusion matrix:'
        print metrics.confusion_matrix(y_test, y_pred)
        print
        print 'Matthew\'s correlation coefficient:',
        print metrics.matthews_corrcoef(y_test, y_pred)
        print

@decorators.Time
def compare_basic_classifiers():
    classifiers = {
        'SVM': svm.SVC(class_weight='auto', kernel='linear'), 
        'Logistic': linear_model.LogisticRegression(C=1e5),
        'Tree': tree.DecisionTreeClassifier(), 
        'KNN': neighbors.KNeighborsClassifier(),
        }
    _compare_classifiers(classifiers)
    
@decorators.Time
def compare_ensemble_classifiers():
    classifiers = {
        'Random Forest': ensemble.RandomForestClassifier(n_estimators=15, 
                                                         max_depth=None),
        'Extreme Trees': ensemble.ExtraTreesClassifier(n_estimators=15,
                                                       max_depth=None,
                                                       min_samples_split=1),
        'Gradient Boost': ensemble.GradientBoostingClassifier(n_estimators=200,
                                                              learn_rate=0.9,
                                                              max_depth=2),
        }
    _compare_classifiers(classifiers)
    
