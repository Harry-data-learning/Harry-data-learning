# ----------------------------------------------------------
# SpaceX Rocket Launch Data Project Script 8
# Purpose: Build ML models to predict Falcon 9 landing success (12 tasks)
# Key Concepts: Standardization, train/test split, logistic regression, SVM, decision tree, KNN, model comparison
# Author: Harry.Zhang
# ----------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

# Plot confusion matrix helper
def plot_confusion_matrix(y, y_predict, title):
    cm = confusion_matrix(y, y_predict)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title(title)
    ax.xaxis.set_ticklabels(['did not land', 'land'])
    ax.yaxis.set_ticklabels(['did not land', 'landed'])
    plt.show()

# Task 1: Load data
X = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv")
data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# Task 2: Extract target variable Y
Y = data['Class'].to_numpy()

# Task 3: Standardize features
transform = preprocessing.StandardScaler()
X = transform.fit_transform(X)

# Task 4: Split train/test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
print("Test sample size:", Y_test.shape[0])

# Task 5: Logistic Regression with GridSearchCV
parameters_lr = {"C": [0.01, 0.1, 1], "penalty": ["l2"], "solver": ["lbfgs"]}
lr = LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters_lr, cv=10)
logreg_cv.fit(X_train, Y_train)
print("[Logistic Regression] Best Params:", logreg_cv.best_params_)
print("Training Accuracy:", logreg_cv.best_score_)
print("Test Accuracy:", logreg_cv.score(X_test, Y_test))
Yhat_lr = logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test, Yhat_lr, "Logistic Regression")

# Task 6: SVM model
parameters_svm = {
    'kernel': ('linear', 'rbf', 'poly', 'sigmoid'),
    'C': np.logspace(-3, 3, 5),
    'gamma': np.logspace(-3, 3, 5)
}
svm = SVC()
svm_cv = GridSearchCV(svm, parameters_svm, cv=10)
svm_cv.fit(X_train, Y_train)
print("[SVM] Best Params:", svm_cv.best_params_)
print("Training Accuracy:", svm_cv.best_score_)
print("Test Accuracy:", svm_cv.score(X_test, Y_test))
Yhat_svm = svm_cv.predict(X_test)
plot_confusion_matrix(Y_test, Yhat_svm, "SVM")

# Task 7: Print best kernel
print("Best kernel used in SVM:", svm_cv.best_params_['kernel'])

# Task 8: Decision Tree model
parameters_tree = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': list(range(1, 10)),
    'max_features': ['auto', 'sqrt'],
    'min_samples_leaf': [1, 2, 4],
    'min_samples_split': [2, 5, 10]
}
tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(tree, parameters_tree, cv=10)
tree_cv.fit(X_train, Y_train)
print("[Decision Tree] Best Params:", tree_cv.best_params_)
print("Training Accuracy:", tree_cv.best_score_)
print("Test Accuracy:", tree_cv.score(X_test, Y_test))
Yhat_tree = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test, Yhat_tree, "Decision Tree")

# Task 9: Print Decision Tree test accuracy
acc_tree = tree_cv.score(X_test, Y_test)
print("Decision Tree Test Accuracy: {:.2%}".format(acc_tree))

# Task 10: KNN model
parameters_knn = {
    'n_neighbors': list(range(1, 11)),
    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
    'p': [1, 2]
}
knn = KNeighborsClassifier()
knn_cv = GridSearchCV(knn, parameters_knn, cv=10)
knn_cv.fit(X_train, Y_train)
print("[KNN] Best Params:", knn_cv.best_params_)
print("Training Accuracy:", knn_cv.best_score_)
print("Test Accuracy:", knn_cv.score(X_test, Y_test))
Yhat_knn = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test, Yhat_knn, "KNN")

# Task 11: Compare models by test accuracy
models = {
    "Logistic Regression": logreg_cv.score(X_test, Y_test),
    "SVM": svm_cv.score(X_test, Y_test),
    "Decision Tree": tree_cv.score(X_test, Y_test),
    "KNN": knn_cv.score(X_test, Y_test)
}

best_model = max(models, key=models.get)
print("Best performing model: {} with accuracy {:.2%}".format(best_model, models[best_model]))

# Task 12: Print accuracy of all models
for model, acc in models.items():
    print(f"{model} Test Accuracy: {acc:.2%}")
