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
import utilities
import features

def _setup(test_size=0.75, classify=True):
    """ Loads and splits the data into training and testing sets.

    - test_size: between 0 and 1, specify the fraction of samples to be
    used for testing. 
    - classify: True if classification task, False if regression task.

    """
    # load dataset
    physio = datasets.load_physio(features.TRY_THIS)
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
    """ Prints performance metrics for a classifier """

    print metrics.classification_report(y_test, y_pred)
    print
    print 'Confusion matrix:'
    print metrics.confusion_matrix(y_test, y_pred)
    print
    print 'Matthew\'s correlation coefficient:',
    print metrics.matthews_corrcoef(y_test, y_pred)
    print 'F1 score:',
    print metrics.f1_score(y_test, y_pred)
    print

def _show_regression_results(y_test, y_pred):
    """ Prints performance metrics for a regressor """

    print 'R^2 score:', metrics.r2_score(y_test, y_pred)
    print 
    print 'MSE:', metrics.mean_squared_error(y_test, y_pred)
    print

def _compare_estimators(estimators, classify=True):
    """ Compares the performance of multiple predictors 
    
    - predictors: a dictionary of estimators, keyed by name
    - classify: True if classifers, False if regressors
    
    """
    X_train, X_test, y_train, y_test = _setup(classify=classify)
    type = 'Classifier' if classify else 'Regressor'
    for name, estimator in estimators.iteritems():
        print '--- {0} {1} ---'.format(name, type)
        estimator.fit(X_train, y_train)
        y_pred = estimator.predict(X_test)
        if classify: 
            _show_classification_results(y_test, y_pred)
        else:
            _show_regression_results(y_test, y_pred)

@utilities.timed
def compare_basic_classifiers():
    """ Compare the performance of simple classifiers. """

    classifiers = {
        'SVM': svm.SVC(class_weight='auto', kernel='linear'), 
        'Logistic': linear_model.LogisticRegression(C=1e5),
        'Tree': tree.DecisionTreeClassifier(), 
        'KNN': neighbors.KNeighborsClassifier(),
        }
    _compare_estimators(classifiers)
    
@utilities.timed
def compare_ensemble_classifiers():
    """ Compare the performance of ensemble classifiers. """

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
    _compare_estimators(classifiers)
   
@utilities.timed
def compare_regressors():
    """ Compare the performance of regressors. """

    regressors = {
        'Linear': linear_model.LinearRegression(),
        'Ridge': linear_model.Ridge(),
        'Lasso': linear_model.Lasso(),
        'LAR': linear_model.Lars(),
        'SGD': linear_model.SGDRegressor(),
        #'ARD': linear_model.ARDRegression() # takes a minute or two
        }
    _compare_estimators(regressors, classify=False)


def _optimize_classifier(param_grid, estimator, score_func):
    """ Searches the parameter space to find the best parameters
    for a given classifier (could be easily generalized to regressors). 

    - param_grid: a dictionary, of list of dictionaries where the
    key is the name of a parameter and the value is a list of values 
    to use for that parameter.
    - estimator: the estimator to optimize
    - score_func: any function that returns a score (float) given two
    1d arrays e.g. score_func(y_true, y_predicted)
    See sklearn's GridSearchCV class.

    """
    
    # parameter search
    X_train, X_test, y_train, y_test = _setup()
    classifier = GridSearchCV(estimator=estimator,
                              param_grid=param_grid,
                              score_func=score_func,
                              n_jobs=1,
                              verbose=2)
    classifier.fit(X_train, y_train, cv=5)

    # print all the scores!
    print
    print 'Tuning hyper-params for', score_func
    print
    print 'Grid scores on training set'
    classifier.grid_scores_.sort(key=lambda x: -x[1]) # sort by descending mean score
    for params, mean_score, scores in classifier.grid_scores_:
        print '{0:3f} (+/- {1:03f}) for {2}'.format(
            mean_score, scores.std() / 2, params)
    print

    print 'Best params found on training set:'
    print '(scoring func: {0})'.format(score_func.__name__)
    print
    print classifier.best_estimator_
    print 
    print '--- Classifier with best params on test set ---'
    
    # test the best estimator that was found
    y_pred = classifier.best_estimator_.predict(X_test)
    _show_classification_results(y_test, y_pred)

@utilities.timed
def optimize_SVC():
    param_grid = [
        { 'class_weight': [None, 'auto'],
          'kernel': ['linear'],
          'C': [1, 2, 5, 10]},        
        { 'class_weight': [None, 'auto'],
          'kernel': ['poly', 'sigmoid'],
          'C': [1, 2, 5],
          'degree': [1, 2, 3, 5],
          'coef0': [0, 0.5, 1, 2],
          'gamma': [0, 1e-6, 1e-4, 1e-2]},
        { 'class_weight': [None, 'auto'],
          'kernel': ['rbf'],
          'C': [1, 2, 5, 10],
          'gamma': [0, 1e-4, 0.1, 1]}
        ]

    # f1_score is weighted by default, e.g class imbalance into account
    _optimize_classifier(param_grid, svm.SVC(), metrics.f1_score)
    
    # could also try matthew's correlation coefficient
    #_optimize_classifier(param_grid, svm.SVC(), metrics.matthews_corrcoef)

@utilities.timed
def optimize_logistic():
    """ Optimize a logistic regression classifier """

    param_grid = {
        'class_weight': [None, 'auto'],
        'penalty': ['l1', 'l2'],
        'C': [1e-6, 1e-3, 1, 2, 4]
        }

    _optimize_classifier(param_grid, linear_model.LogisticRegression(), metrics.f1_score) 
    _optimize_classifier(param_grid, linear_model.LogisticRegression(), metrics.matthews_corrcoef)


    
    
