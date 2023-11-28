import streamlit as st
import pandas as pd
import numpy as np

st.title("Art Valuation App \U0001F3A8")
st.header('CS Project by Group 2.2')
df = pd.read_csv(r"C:\Users\loren\OneDrive\Documents\5 Semester\CS\Groupe project\cleaned_tow.csv")


#hello world

# new columns name
names_new_columns = {'artist_name':'Artist Name','year_artist_born':'Birth year','age':'Age','length':'Length','width':'Width','title_of_work':'Title','height':'Height'
                     ,'year_of_work':'Creation Year','age_at_work':'Age of Artist at Creation','lower_est_USD':'Lower est. USD','upper_est_USD':'Upper est. USD',
                     'sold_in_USD':'Sales Amount in USD','Material_Category':'Material Category','act_area':'Act. Area','posthumous_combined':'Posthumous Combined'}
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
    filtered_df = filtered_df[filtered_df['Artist Name'].str.contains(artist_name_input, case=False)]

# Show search result summary
st.subheader("Results of your Search")
if artist_name_input:
    st.write(f"Showing artworks by artist(s) containing '{artist_name_input}':")
    st.write(filtered_df)
else:
    st.write("Please enter an artist's name (or part of it) to perform a search.")



st.header('Filter for artworks by price')
# checkbox to filter posthumous artworks
posthumous_checkbox = st.checkbox("Filter Posthumous Artworks")

# extract Sales Amount in USD column, remove unnecessary caracters, and convert to float
sold_in_usd = df['Sales Amount in USD']

# slider to filter based on sold_in_USD
min_price, max_price = st.slider("Filter by Price Range", 
                                min_value=float(sold_in_usd.min()),
                                max_value=float(sold_in_usd.max()),
                                value=(float(0), float(sold_in_usd.max())))

# filter the dataframe based on the checkbox and slider values
filtered_2_df = df.copy()

if posthumous_checkbox:
    # only true is considered posthumous
    filtered_2_df = filtered_2_df[filtered_2_df['Posthumous Combined'].isin([1])]

filtered_2_df['Sales Amount in USD'] = sold_in_usd
filtered_2_df = filtered_2_df[(filtered_2_df['Sales Amount in USD'] >= min_price) & (filtered_2_df['Sales Amount in USD'] <= max_price)]

# Display the dataframe
st.write("Filtered Artworks:")
st.write(filtered_2_df)

st.header('Filter for artworks by Material Category')
