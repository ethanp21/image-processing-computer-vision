# linear approach to modeling the relationship between a scalar response (or dependent variable)
# and one or more explanatory variables (or independent variables)
# uses multiple independant variables and fits a linear line to the data to estimate a coorelated dependant variable



import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style

data = pd.read_csv("student-mat.csv", sep=";")

data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]

print(data.head())

predict = "G3"

training_Data = np.array(data.drop([predict], 1))
outputs = np.array(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(training_Data, outputs, test_size= 0.1)

linear = linear_model.LinearRegression()

linear.fit(x_train,y_train)
accuracy = linear.score(x_test,y_test)

print("accuracy is: " , accuracy)
print("coefficitents are: " , str(linear.coef_))
print("intercept is: " , linear.intercept_ )

predictions = linear.predict(x_test)

for x in range(len(predictions)):
    print(predictions[x], x_test[x], y_test[x])

p = 'studytime'
style.use("ggplot")
pyplot.scatter(data[p],data["G3"])
pyplot.xlabel(p)
pyplot.ylabel("Final Grade")
pyplot.show()




