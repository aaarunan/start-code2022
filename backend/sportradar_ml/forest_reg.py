from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz
from sklearn.metrics import mean_squared_error
from tabulate import tabulate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydot

"""
One-hot encoding:

Convert the data into usable, machine-language: array of binary. 
A one represents a boolean value true for a given parameter.
This can be done using pandas' dataframe.

"""

df = pd.DataFrame()

df = pd.get_dummies()

# Check pd.get_dummies()

# Separate features (input values) and target (desired output value)

labels = np.array(df['Goals'])

df = df.drop(df['Goals'])

list_features = list(df.columns)

features = np.array(df)

# Split data into training (approx. 70-80%) and testing (20-30%) sets.

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.20,
                                                                            random_state=42)

rf = RandomForestRegressor(n_estimators=1000, random_state=42)

# Train the model using the training set's features and labels
rf.fit(features, labels)

predictions = rf.predict(test_features)
errors = abs(predictions - test_labels)
MAE = round(np.mean(errors), 2)

"""
After training the algorithm, it would be nice with some overview of the factors as well as what a random forest
really is.
"""

def print_tree():
    # Pull out one tree from the forest
    tree = rf.estimators_[5]
    # Export the image to a dot file
    export_graphviz(tree, out_file='tree.dot', feature_names=list_features, rounded=True, precision=1)
    # Use dot file to create a graph
    (graph,) = pydot.graph_from_dot_file('tree.dot')
    # Write graph to a png file
    graph.write_png('tree.png')

def find_MSE():
    return mean_squared_error(predictions, test_labels)

def find_RMSE():
    return np.sqrt(find_MSE())

def get_stat_table():
    table = [["MSE", "RMSE"]]

    # Get the different weightings of features
importances = list(rf.feature_importances_)

# Making a graph of all the important factors for creating a prediction.
def graph_feature_importance():
    plt.style.use('Solarize_Light2')
    x_values = list(range(len(importances)))
    plt.bar(x_values, importances, orientation='vertical')
    plt.xticks(x_values, list_features, rotation='vertical')    # Tick labels for x axis
    # Axis labels and title
    plt.ylabel('Weighting/Importance of factor')
    plt.xlabel('Features')
    plt.title('Importance of Variables')

"""
Now, there needs to be a way to feed in a single feature update into the algorithm and get a new, adjusted value result
"""


def get_new_prediction(new_event):
    # Input to handle: time in game, the actual event
    return rf.predict(new_event)
