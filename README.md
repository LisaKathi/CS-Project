# CS-Project
The group project for the Computer Science course at the University of St. Gallen.

Overview of the Notebooks / Python files & Dataframes:

1) Original Dataset
Source: https://data.mendeley.com/datasets/2nfvz8g27c/1
- AppraiSet_complete_dataset.csv: the complete original dataset used for our data cleaning.
- AppraiSet_testing_dataset.csv: the orginial testing dataset, not actively used -> we wanted to clean the data ourselves to better fit our project needs
- AppraiSet_training_dataset.csv: the original training dataset, not actively used -> we wanted to clean the data ourselves to better fit our project needs

2) Data Clearning and Machine Learning Model
Code
1_Notebook.ipynb: majority of the data cleaning including material category
artist_name.ipynb: final data cleaning including arist_rank and the development of our ML model
Artiste_name(streamlitteam).py: integration of the machine learning model into streamlit
Dataframes
cleaned.csv: Our cleaned dataset used in final project
cleaned_tow.csv: Our cleaned dataset + column title of work 

3) First attemps at Streamlit
myapp.py : first attempt at making a streamlit app, not used in final project
test_björn.py: testing streamlit functions, not used in final project
test_lorenzo.py: testing streamlit functions, not used in final project
fiona_update.py: improving sliders and filters with streamlit 

4) API Inclusion
StreamlitAPI_combined.py : not used in final project, first attempt at the integration of the two apis (artsy and google)
2 api.py : combined google api and artsy api, artsy to search for artist info and google for image search
artsy_google_api.py : final version of the two apis, used in final project

5) Creating a final product
Streamlit_DataDiscovery_Prediction_combined.py: First attempt at combining prediction and data discovery with ML model, and combined API 
myappfinal.py: Our final streamlit product, including the Prediction, Data Discovery, API usage and Visualization pages plus the final design








