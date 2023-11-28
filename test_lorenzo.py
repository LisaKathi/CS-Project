import streamlit as st
import pandas as pd
import numpy as np

st.title("Art Valuation App \U0001F3A8")
st.header('CS Project by Group 2.2')
df = pd.read_csv(r"C:\Users\loren\Downloads\AppraiSet_complete_dataset.csv")


#hello world

# new columns name
names_new_columns = {'artist_name':'Artist Name','year_artist_born':'Birth year','year_of_death':'Death Year','age':'Age','title_of_work': 'Title','materials':'Materials',
                     'length:':'Length','width':'Width','height':'Height','area':'Area','measurement_2':'Measurement 2','length_2':'Length 2','width_2':'Width 2',
                     'height_2':'Height 2','area_2':'Area 2','measurement_3':'Measurement 3', 'length_3':'Length 3', 'width_3':'Width 3','height_3':'Height 3',
                     'area_3':'Area 3', 'unit_cm':'Unit in cm','year_of_work':'Creation Year','age_at_work':'Age of Artist at Creation','note':'Comment','lower_estimate':'Lower Estimate',
                     'upper_estimate':'Upper Estimate','amount_sold':'Sales Amount','currency':'Currency','sold_T_or_F':'Sold T or F','lower_est_USD':'Lower est. USD',
                     'upper_est_USD':'Upper est. USD','sold_in_USD':'Sales Amount in USD','posthumous_T_or_F_or_U':'Posthumous T or F or U'}
df.rename(columns=names_new_columns, inplace= True)


#SLIDER FOR YEAR OF WORK RANGE#
##### we need to convert Creation Year to numeric, because otherwise compares int with string####
st.header('Filter for artworks by year')
df['Creation Year'] = pd.to_numeric(df['Creation Year'], errors='coerce')

# Year range slider code 
min_year = int(df['Creation Year'].min()) if not pd.isnull(df['Creation Year']).all() else 0
max_year = int(df['Creation Year'].max()) if not pd.isnull(df['Creation Year']).all() else 0
selected_years = st.slider("Select a range of years", min_year, max_year, (min_year, max_year))


# filtered df by year of work and display on the app
filtered_df = df[
    (df['Creation Year'] >= selected_years[0]) & 
    (df['Creation Year'] <= selected_years[1])
]

st.subheader("Filtered Data:")
st.write(filtered_df)

# Counter for the number of artworks in the selected range
num_artworks = filtered_df.shape[0]
st.markdown(f"Number of Artworks in Selected Range: **{num_artworks}**")

### TEXT INPUT BOX for ARTIST NAME SEARCH ######3
st.header('Search for an artist by name')
artist_name_input = st.text_input("Please enter an artist's name (or part of the name):")
if artist_name_input:
    filtered_df = filtered_df[filtered_df['artist_name'].str.contains(artist_name_input, case=False)]

# Show search result summary
st.subheader("Results of your Search")
if artist_name_input:
    st.write(f"Showing artworks by artist(s) containing '{artist_name_input}':")
    st.write(filtered_df)
else:
    st.write("Please enter an artist's name (or part of it) to perform a search.")




# checkbox to filter posthumous artworks
posthumous_checkbox = st.checkbox("Filter Posthumous Artworks")

# extract Sales Amount in USD column, remove unnecessary caracters, and convert to float
sold_in_usd = df['Sales Amount in USD'].str.replace('$', '').str.replace(',', '').astype(float)

# slider to filter based on sold_in_USD
min_price, max_price = st.slider("Filter by Price Range", 
                                min_value=float(sold_in_usd.min()),
                                max_value=float(sold_in_usd.max()),
                                value=(float(0), float(sold_in_usd.max())))

# filter the dataframe based on the checkbox and slider values
filtered_2_df = df.copy()

if posthumous_checkbox:
    # only true is considered posthumous
    filtered_2_df = filtered_2_df[filtered_2_df['Posthumous T or F or U'].isin(['TRUE'])]

filtered_2_df['Sales Amount in USD'] = sold_in_usd
filtered_2_df = filtered_2_df[(filtered_2_df['Sales Amount in USD'] >= min_price) & (filtered_2_df['Sales Amount in USD'] <= max_price)]

# Display the dataframe
st.write("Filtered Artworks:")
st.write(filtered_2_df)
