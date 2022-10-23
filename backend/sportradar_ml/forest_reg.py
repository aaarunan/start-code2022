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


def get_df_from_csv(file_name):
    return pd.read_csv("../matches/" + file_name + ".csv")


"""
One-hot encoding:

Convert the data into usable, machine-language: array of binary. 
A one represents a boolean value true for a given parameter.
This can be done using pandas' dataframe.

"""


# Separate features (input values) and target (desired output value)

def get_labels(df):
    """
    This method gets the label from the dataframe.
    """
    return np.array(df['FINAL GOALS'])


def drop_label(df):
    """
    This method removes the label from the dataframe.
    """
    return df.drop(columns=['FINAL GOALS', 'RED CARD', 'PENALTY AWARDED'])


def get_list_of_features(df):
    """
    This method gets a list of the features from the dataframe.
    """
    return list(drop_label(df).columns)


def get_arr_features(df):
    """
    This method gets an array of the features from the dataframe.
    """
    return np.array(drop_label(df))


def split_data(features, labels):
    """
    Split data into training (approx. 70-80%) and testing (20-30%) sets. This is called hold-out validation.
    The train_test_split method automatically randomly splits the data set based on the random_state variable.
    """
    return train_test_split(features, labels, test_size=0.5, random_state=42)


# Could switch verbose back to one, check when the algorithm is actually being used.
def create_forest():
    """
    This method creates a random forest regressor, with 1000 decision trees, random validation and display information
    surrounding the building of trees.
    """
    return RandomForestRegressor(n_estimators=1500, random_state=42, verbose=2)


def train_rf(rf):
    """
    This method trains the model.
    """
    rf.fit(get_arr_features(df), get_labels(df))


# Train the model using the training set's features and labels

def save_trained_model(rf, name_of_file):
    """
    This method saves the trained model, given the model and the file name.
    """
    joblib.dump(rf, str(name_of_file) + ".joblib")


def load_model_from_joblib(name_of_file):
    """
    This method loads a model, given the file name of the joblib.
    """
    path = name_of_file + ".joblib"
    if os.path.exists(path):
        return joblib.load(path)


def get_important_feat(rf):
    """
    After training the algorithm, it would be nice with some overview of the factors as well as what a random forest
    really is.
    """
    return list(rf.feature_importances_)


def calc_MSE():
    """
    This method calculates the mean squared error of the prediction from the model versus the actual values,
    """
    return mean_squared_error(predictions, test_labels)


def calc_MAE():
    """
    This method calculates the mean absolute error of the prediction from the model versus the actual values.
    """
    errors = abs(predictions - test_labels)
    mae = (1 / len(errors)) * sum(errors)
    return mae


def calc_RMSE():
    """
    This method calculates the mean squared error of the prediction from the model versus the actual values,
    """
    return np.sqrt(calc_MSE())


def calc_R_Squared():
    """
    This method calculates the coefficient of determination, R-squared.
    """
    return rf.score(test_features, test_labels)


def get_stat_table():
    """
    This method creates a table containing information about the accuracy of the trained model.

    Lower values of MAE, MSE, and RMSE indicates a higher accuracy
    A higher coefficient of determination R square is also desirable.
    """
    table = [["MSE", "MAE", "RMSE", "R-squared"], [calc_MSE(), calc_MAE(), calc_RMSE(), calc_R_Squared()]]
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))


def print_tree():
    """
    This method creates and saves a png of a chosen decision tree.
    """
    # Pull out one tree from the forest
    tree = rf.estimators_[5]
    # Export the image to a dot file
    export_graphviz(tree, out_file='tree.dot', feature_names=get_list_of_features(df), rounded=True, precision=1)
    # Use dot file to create a graph
    (graph,) = pydot.graph_from_dot_file('tree.dot')
    # Write graph to a png file
    graph.write_png('tree.png')


def graph_feature_importance():
    """
    This method creates a bar graph displaying the relative importance/weightings of the different features.
    """
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


def get_new_prediction(new_event_df, rf):
    """
    By taking a new event dataframe as a parameter, this method returns the algorithm's best prediction for the final
    score of one team.
    """
    new_event_df = drop_label(new_event_df)
    # Input to handle: time in game, the actual event
    return rf.predict(new_event_df)


# def test_model(rf):
#     df_test = get_df_from_csv("300matches")
#     label_from_test = get_labels(df_test) #     feat_from_test = get_list_of_features(df_test)
#     predictions = rf.predict(feat_from_test)
#     print(predictions)
#     print(label_from_test)


if __name__ == '__main__':
    print("Loading data...")
    df = get_df_from_csv("1000matches")
    train_features, test_features, train_labels, test_labels = split_data(get_arr_features(df), get_labels(df))

    print("Creating model...")
    rf = create_forest()
    train_rf(rf)
    save_trained_model(rf, "rf")

    # print("Loading model...")
    # rf = load_model_from_joblib("../rf")

    print("Calculating predictions...")
    predictions = rf.predict(test_features)

    print("Calculating importance...")
    importances = get_important_feat(rf)

    # print_tree()
    graph_feature_importance()
    get_stat_table()
    print("Predictions")
    print(predictions)
    print("Actual Values")
    print(test_labels)
