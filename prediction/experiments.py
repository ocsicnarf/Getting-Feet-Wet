import time
import pylab as pl
import numpy as np
from sklearn import svm, neighbors, tree, linear_model, metrics
from sklearn import ensemble
from sklearn import cross_validation
from sklearn import preprocessing
from sklearn.grid_search import GridSearchCV
import datafiles
import datasets
import decorators

def _setup(test_size=0.75, classify=True):
    # load dataset
    physio = datasets.load_physio_stats()
    X = physio.data
    y = physio.c_target if classify else physio.r_target
    n_samples = X.shape[0]

    # normalize features (SVM classifier trains much much faster)
    X = preprocessing.scale(X) # zero mean, unit variance
    
    # construct training and testing sets
    X_train, X_test, y_train, y_test =\
        cross_validation.train_test_split(X, y, test_size=test_size)
    
    return X_train, X_test, y_train, y_test

           
def _show_classification_results(y_test, y_pred):
    print metrics.classification_report(y_test, y_pred)
    print
    print 'Confusion matrix:'
    print metrics.confusion_matrix(y_test, y_pred)
    print
    print 'Matthew\'s correlation coefficient:',
    print metrics.matthews_corrcoef(y_test, y_pred)
    print

def _show_regression_results(y_test, y_pred):
    print 'R^2 score:', metrics.r2_score(y_test, y_pred)
    print 
    print 'MSE:', metrics.mean_squared_error(y_test, y_pred)
    print

def _compare_predictors(predictors, classify=True):
    X_train, X_test, y_train, y_test = _setup(classify=classify)
    type = 'Classifier' if classify else 'Regressor'
    for name, c in predictors.iteritems():
        print '--- {0} {1} ---'.format(name, type)
        start = time.time()
        c.fit(X_train, y_train)
        y_pred = c.predict(X_test)
        if classify: 
            _show_classification_results(y_test, y_pred)
        else:
            _show_regression_results(y_test, y_pred)

@decorators.Time
def compare_basic_classifiers():
    classifiers = {
        'SVM': svm.SVC(class_weight='auto', kernel='linear'), 
        'Logistic': linear_model.LogisticRegression(C=1e5),
        'Tree': tree.DecisionTreeClassifier(), 
        'KNN': neighbors.KNeighborsClassifier(),
        }
    _compare_predictors(classifiers)
    
@decorators.Time
def compare_ensemble_classifiers():
    classifiers = {
        'Random Forest': ensemble.RandomForestClassifier(
            n_estimators=15, 
            max_depth=None),
        'Extreme Trees': ensemble.ExtraTreesClassifier(
            n_estimators=15, 
            max_depth=None, 
            min_samples_split=1),
        'Gradient Boost': ensemble.GradientBoostingClassifier(
            n_estimators=100, 
            learn_rate=0.9, 
            max_depth=3),
        }
    _compare_predictors(classifiers)
    

@decorators.Time
def compare_regressors():
    regressors = {
        'Linear': linear_model.LinearRegression(),
        'Ridge': linear_model.Ridge(),
        'Lasso': linear_model.Lasso(),
        'LAR': linear_model.Lars(),
        'SGD': linear_model.SGDRegressor(),
        'ARD': linear_model.ARDRegression() # takes a minute or two
        }
    _compare_predictors(regressors, classify=False)


@decorators.Time
def optimize_SVC():
    X_train, X_test, y_train, y_test = _setup()
    param_grid = [
        { 'class_weight': [None, 'auto'],
          'kernel': ['linear'],
          'C': [1, 2, 5, 10]},        
        { 'class_weight': [None, 'auto'],
          'kernel': ['poly', 'sigmoid'],
          'C': [1, 2, 5, 10],
          'degree': [1, 2, 3, 5],
          'coef0': [0, 0.5, 1, 2],
          'gamma': [0, 1e-6, 1e-4, 1e-2]},
        { 'class_weight': [None, 'auto'],
          'kernel': ['rbf'],
          'C': [1, 2, 5, 10],
          'gamma': [0, 1e-4, 0.1, 1]},
        ]

    print 'Tuning hyper-params for Matthew\'s Correlation Coefficient'
    classifier = GridSearchCV(estimator=svm.SVC(),
                              param_grid=param_grid,
                              score_func=metrics.matthews_corrcoef,
                              n_jobs=10,
                              verbose=2)
    classifier.fit(X_train, y_train, cv=5)
    
    print 'Best params found on training set:'
    print
    print classifier.best_estimator_
    print 
    print 'Grid scores on training set'
    classifier.grid_scores_.sort(key=lambda x: -x[1]) # sort by descending mean score
    for params, mean_score, scores in classifier.grid_scores_:
        print '{0:3f} (+/- {1:03f}) for {2}'.format(
            mean_score, scores.std() / 2, params)
    print

    print '--- Best SVM Classifier ---'
    print 'Params:', classifier.grid_scores_[0][0]
    y_pred = classifier.best_estimator_.predict(X_test)
    _show_results(y_test, y_pred)
