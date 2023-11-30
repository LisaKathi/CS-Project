# %%
# importing pandas and defining the cleaned dataset as df
import pandas as pd
df = pd.read_csv(r"C:\Users\loren\OneDrive\Documents\5 Semester\CS\Groupe project\cleaned.csv")
df


# %%
# creating a new column by calculating the average of the lower and upper estimate value
df["average_est_USD"] = ((df["lower_est_USD"] + df["upper_est_USD"]) / 2 )
df

# %%
# using groupby to calculate the average estimation value of all artworks for each artist
# this is done to capture the differences between artists since we cannot use the column "artist_name" since it is categorical information
grouped = df.groupby("artist_name").agg({'average_est_USD': ['mean', 'count']}).round(2)
grouped

# %%
# finding the values for the 10th, 20th, 30th, 40th, 50th, 60th, 70th, 80th and 90th percentile
import numpy as np
percentile_values = np.percentile(grouped["average_est_USD"]["mean"], [10, 20, 30, 40, 50, 60, 70, 80, 90])
percentile_values

# %%

# using n.digitize to assign bins
rank = np.digitize(grouped["average_est_USD"]["mean"], bins=percentile_values, right=True) 
# got the idea to use .digitize from ChatGPT to improve my prior code
# the prior code consisted of a loop that checked if i <= than each of the percentile_values and > than the last percentile value
# then it appended the according rank to the rank list

# making sure the ranks start from 1 instead of 0
rank += 1

# changing the array to a list
rank_list = rank.tolist()
rank_list

# %%
# creating a new column called "rank" to assign the values from the rank list to the grouped dataframe
grouped["rank"] = rank_list
grouped = grouped[["rank"]]
grouped

#changing the grouped dataframe to a dictionary to add it to df later
rank_dict = grouped.to_dict()
# getting rid of the outer dictionary so it's not a nested dictionary and we have the values we want in the shape we want
rank_dict = rank_dict[('rank', '')]
rank_dict

# %%
# using the map function to assign the values from the rank_dict to a new column called "artist_rank"
df["artist_rank"] = df['artist_name'].map(rank_dict)

# inspecting the distribution of ranks
df["artist_rank"].value_counts()

# %%
# inspecting the distribution of artists
df["artist_name"].value_counts()

# %%
# checking to see if all columns are present that we want to have
df

# %%
# dropping the columns "average_est_USD" and "artist_name" since they fulfilled their purpose and will not be part of the ML model
df = df.drop(columns=["average_est_USD", "artist_name"])
df

# %%
# defining which columns we want to change from floats to integers
float_to_int = ['year_artist_born', 'age', 'year_of_work', "age_at_work"]
# changing the desired columns to integers 
df[float_to_int] = df[float_to_int].astype(int)
df

# %%
# now for the comparison of different models to see which one is best for our purpose we import the models
# in addition we import train_test_split to split the data easily into training and test data
# and some metrics to evaluate how well our models did plus the matplotlib library for plotting our results
# this is probably a good point to mention that I know these models from prior courses (Business Analytics / Machine Learning & DSF)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# defining our variables (X) and target value (y)
X = df.drop(columns="sold_in_USD")
y = df["sold_in_USD"]

# splitting the data into training and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


# initializing our models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(),
    "Gradient Boosting": GradientBoostingRegressor(),
}
# ChatGPT gave me the idea to combine the models in a list and let it run through a loop for a more efficient comparison 
# instead of trying each model out one after the other


# creating a template for our results
results = {"Model": [], "RMSE": [], "R^2": []}

# creating a loop for training and evaluating the models
for name, model in models.items():
    # training the model on the training data
    model.fit(X_train, y_train)

    # using the trained model to give a prediction on the testing data
    y_pred = model.predict(X_test)

    # using our performance metrics rmse (root mean squared error) and r^2 (seeing what amoun)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)

    # saving our results in our template
    results["Model"].append(name)
    results["RMSE"].append(rmse)
    results["R^2"].append(r2)

# creating a df out of our results template
results_df = pd.DataFrame(results)

# showing the df
print(results_df)

# creating a plot
fig, ax = plt.subplots()
# making it bar chart
ax.bar(results_df["Model"], results_df["R^2"], color="green", alpha=0.7)
# setting a title and labels for the x and y axis
ax.set_title("Model Comparison")
ax.set_xlabel("Model")
ax.set_ylabel("R^2")

plt.show()

# %%
# now that we know that the random forest and gradient boosting model perform both quite close to each other
# we chose the random forest model for the streamlit prediction because it performs almost as well as gradient boosting
# but random forest loads quicker and is considered a more robust model

# defining our variables (X) and target value (y)
X = df.drop(columns="sold_in_USD")
y = df["sold_in_USD"]

# splitting the data into training and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# establishing a Random Forest model and training it on the training data
model = RandomForestRegressor()
model.fit(X_train, y_train)

# using the trained model to give a prediction on the testing data
y_pred = model.predict(X_test)

# STREAMLIT TEAM from here one the integration is yours

# %%
#Save and Training Instances 
path = r'C:\Users\loren\OneDrive\Documents\5 Semester\CS\Groupe project\My first app'
df.loc[X_train.index,:].to_csv(path + "prosper_data_app_dev.csv", index = False)
df.loc[X_test.index,:].drop("sold_in_USD", axis = 1).to_csv(path + "new_customers.csv", index = False)

# %%
import pickle 
filename = "finalized_artworks_prediction.sav"
pickle.dump(model, open(filename, "wb"))

# %%
new_artworks = pd.read_csv(path + "new_customers.csv")
new_artworks = pd.get_dummies(new_artworks, drop_first = True) 
new_artworks 

# %%
loaded_model = pickle.load(open(filename,"rb"))
loaded_model. predict(new_artworks)

# %%
# now to visualize the success of our model we are visualizing it

# finding the min and max value between the actual values and our prediction 
min_value=np.array([y_test.min(), y_pred.min()]).min()
max_value=np.array([y_test.max(), y_pred.max()]).max()

# creating a scatter plot to show the relationship between our predicted and actual values
# and creating a line to separate the sphere of actual values from the sphere of the predicted values
fig, ax = plt.subplots()
ax.scatter(y_test,y_pred, color="blue", alpha=0.2)
ax.plot([min_value,max_value], [min_value, max_value], lw=1, color="green")

# setting title and axis labels
ax.set_title("Actual vs Predicted Values")
ax.set_xlabel('Actual')
ax.set_ylabel('Predicted')

plt.show()


# %%
# changing the code for the plot to shrink the window of values that we see since most values seem to be < 500 000
# the idea to use a limit parameter came from ChatGPT, as well as the use of .set_xlim and .set_ylim

def actual_vs_predicted_plot(y_true, y_pred, limit):

    # finding the min and max value between the actual values and our prediction
    min_value = np.array([y_true.min(), y_pred.min()]).min()
    max_value = np.array([y_true.max(), y_pred.max()]).max()

    # defining the limit and min_value by making sure that the limit is not bigger than the max value or smaller than the min value
    limit = min(limit, max_value) 
    min_value = min(min_value, limit)
    
    # creating a scatter plot and a line to visualize our performance
    fig, ax = plt.subplots()
    ax.scatter(y_true, y_pred, color="blue", alpha=0.2)
    ax.plot([min_value, limit], [min_value, limit], lw=1, color="green")

    # setting title and axis labels
    ax.set_title("Actual vs Predicted Values")
    ax.set_xlabel('Actual')
    ax.set_ylabel('Predicted')

    # setting the x and y axis limits
    ax.set_xlim([min_value, limit])
    ax.set_ylim([min_value, limit])

    plt.show()

# %%
# the plot for values up to 500 000
actual_vs_predicted_plot(y_test, y_pred, limit=500000)

# %%
# the plot for values up to 100 000
actual_vs_predicted_plot(y_test, y_pred, limit=100000)

# %%
# the plot for values up to 20 000
actual_vs_predicted_plot(y_test, y_pred, limit=20000)

# %%
