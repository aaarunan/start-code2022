import os

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz
from sklearn.metrics import mean_squared_error
from tabulate import tabulate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydot

os.chdir('..')


def get_df_from_csv():
    return pd.read_csv("matches/1000matches.csv")


"""
One-hot encoding:

Convert the data into usable, machine-language: array of binary. 
A one represents a boolean value true for a given parameter.
This can be done using pandas' dataframe.

"""

df = get_df_from_csv()


# Separate features (input values) and target (desired output value)

def get_labels(df):
    return np.array(df['FINAL GOALS'])


def drop_label(df):
    return df.drop(columns=['FINAL GOALS'])


def get_list_of_features(df):
    return list(drop_label(df).columns)


def get_arr_features(df):
    return np.array(drop_label(df))


# Split data into training (approx. 70-80%) and testing (20-30%) sets. This is called hold-out validation.
# The train_test_split method automatically randomly splits the data set based on the random_state variable.

def split_data(features, labels):
    return train_test_split(features, labels, test_size=0.95, random_state=42)


train_features, test_features, train_labels, test_labels = split_data(get_arr_features(df), get_labels(df))


# Could switch verbose back to one, check when the algorithm is actually being used.
def create_forest():
    return RandomForestRegressor(n_estimators=1000, random_state=42, verbose=2)


rf = create_forest()


def train_rf(rf):
    rf.fit(get_arr_features(df), get_labels(df))


train_rf(rf)


# Train the model using the training set's features and labels

def save_trained_model(rf, name_of_file):
    joblib.dump(rf, str(name_of_file) + ".joblib")


save_trained_model(rf, "Trained_random_forest")


def load_model(name_of_file):
    path = name_of_file + ".joblib"
    if os.path.exists(path):
        return joblib.load(path)


predictions = rf.predict(test_features)

"""
After training the algorithm, it would be nice with some overview of the factors as well as what a random forest
really is.
"""


def get_important_feat(rf):
    return list(rf.feature_importances_)

importances = get_important_feat(rf)


def print_tree():
    # Pull out one tree from the forest
    tree = rf.estimators_[5]
    # Export the image to a dot file
    export_graphviz(tree, out_file='tree.dot', feature_names=get_list_of_features(df), rounded=True, precision=1)
    # Use dot file to create a graph
    (graph,) = pydot.graph_from_dot_file('tree.dot')
    # Write graph to a png file
    graph.write_png('tree.png')


def calc_MSE():
    return mean_squared_error(predictions, test_labels)


def calc_MAE():
    errors = abs(predictions - test_labels)
    mae = 1 / len(errors) * sum(errors)
    return mae


def calc_RMSE():
    return np.sqrt(calc_MSE())


def calc_R_Squared():
    return rf.score(test_features, test_labels)


def compare_predict_to_real():
    table = [["Real Value", "Prediction"], test_labels, predictions]


"""
    Lower values of MAE, MSE, and RMSE indicates a higher accuracy
    A higher coefficient of determination R square is also desirable.
"""


def get_stat_table():
    table = [["MSE", "MAE", "RMSE", "R-squared"], [calc_MSE(), calc_MAE(), calc_RMSE(), calc_R_Squared()]]
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))


"""
This method creates a table containing information about the accuracy of the trained model.
"""


def graph_feature_importance():
    plt.style.use('Solarize_Light2')
    x_values = list(range(len(importances)))
    plt.bar(x_values, importances, orientation='vertical')
    plt.xticks(x_values, get_list_of_features(df), rotation='vertical')  # Tick labels for x axis
    # Axis labels and title
    plt.ylabel('Weighting/Importance of factor')
    plt.xlabel('Features')
    plt.title('Importance of Variables')
    plt.tight_layout()
    plt.show()


"""
This method creates a bar graph displaying the relative importance/weightings of the different features.
"""


def get_new_prediction(new_event_df):
    # Input to handle: time in game, the actual event
    return rf.predict(new_event_df)


"""
By taking a new event dataframe as a parameter, this method returns the algorithm's best prediction for the final score 
of one team.
"""

if __name__ == '__main__':
    # print_tree()
    graph_feature_importance()
    get_stat_table()
    print("Predictions")
    print(predictions)
    print("Actual Values")
    print(test_labels)
