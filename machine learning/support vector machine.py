# program to find the largest distance between "support vectors", this will find the best
# hyperplane which is a linear fit in between the data
# and that will be used to split data and classify the targets




import sklearn
from sklearn import datasets
from sklearn import svm
from sklearn import metrics
import matplotlib.pyplot as pyplot
from matplotlib import style

cancer = datasets.load_breast_cancer()

print(cancer.feature_names) #features
print(cancer.target_names) #lavels or targets

x = cancer.data
y = cancer.target

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2) # create the data


# implement classifier using a linear kernel to parse data
clf = svm.SVC(kernel="linear")
clf.fit(x_train, y_train)

y_pred = clf.predict(x_test)


# calculate accuracy
acc = metrics.accuracy_score(y_test, y_pred)

print(acc)

names = ['malignant', 'benign']


for x in range(len(y_pred)):
    print("Predicted: ", names[y_pred[x]], "Data: ", x_test[x], "Actual: ", names[y_test[x]])
