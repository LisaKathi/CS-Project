import streamlit as st
import pandas as pd

st.title("Art Valuation App \U0001F3A8")
st.header('CS Project by Group 2.2')
df = pd.read_csv(r"C:\Users\loren\Downloads\AppraiSet_complete_dataset.csv")

#SLIDER FOR YEAR OF WORK RANGE#
##### we need to convert year_of_work to numeric, because otherwise compares int with string####
st.header('Filter for artworks by year')
df['year_of_work'] = pd.to_numeric(df['year_of_work'], errors='coerce')

# Year range slider code 
min_year = int(df['year_of_work'].min()) if not pd.isnull(df['year_of_work']).all() else 0
max_year = int(df['year_of_work'].max()) if not pd.isnull(df['year_of_work']).all() else 0
selected_years = st.slider("Select a range of years", min_year, max_year, (min_year, max_year))


# filtered df by year of work and display on the app
filtered_df = df[
    (df['year_of_work'] >= selected_years[0]) & 
    (df['year_of_work'] <= selected_years[1])
]


st.subheader("Filtered Data:")
st.write(filtered_df)

# Counter for the number of artworks in the selected range
num_artworks = filtered_df.shape[0]
st.markdown(f"Number of Artworks in Selected Range: **{num_artworks}**")

# new columns name
names_new_columns = {'artist_name':'Artist Name','year_artist_born':'Birth year','year_of_death':'Death Year','age':'Age','title_of_work': 'Title','materials':'Materials',
                     'length:':'Length','width':'Width','height':'Height','area':'Area','measurement_2':'Measurement 2','length_2':'Length 2','width_2':'Width 2',
                     'height_2':'Height 2','area_2':'Area 2','measurement_3':'Measurement 3', 'length_3':'Length 3', 'width_3':'Width 3','height_3':'Height 3',
                     'area_3':'Area 3', 'unit_cm':'Unit in cm','year_of_work':'Creation Year','age_at_work':'Age of Artist at Creation','note':'Comment','lower_estimate':'Lower Estimate',
                     'upper_estimate':'Upper Estimate','amount_sold':'Sales Amount','currency':'Currency','sold_T_or_F':'Sold T or F','lower_est_USD':'Lower est. USD',
                     'upper_est_USD':'Upper est. USD','sold_in_USD':'Sales Amount in USD','posthumous_T_or_F_or_U':'Posthumous T or F or U'}
df.rename(columns=names_new_columns, inplace= True)

st.write("With new columns")
st.write(df)

# Define dataframe Code isn't all complete 
data = pd.read_csv(r"C:\Users\loren\Downloads\AppraiSet_complete_dataset.csv")

# Function to filter data
def filter_data(data, filter_value):
    filtered_data = data[data["materials"].isin(filter_value)]
    return filtered_data

# Streamlit app
st.title("Filter Data by Checkbox")

# Display dataframe
st.write(data)

# Define filter options
filter_options = ['oil on canvas', 'acrylic','embroidery','tempera','watercolor']

# Display filter options
filter_value = st.multiselect("Select materials to filter", filter_options)

# Apply filter based on multiselect value
if filter_value:
    filtered_data = filter_data(data, filter_value)
    st.write(filtered_data)
