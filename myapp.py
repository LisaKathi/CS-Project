import streamlit as st
import pandas as pd

st.title("Art Valuation App \U0001F3A8")
st.header('CS Project by Group 2.2')
df = pd.read_csv(r"C:\Users\ioles\Downloads\AppraiSet_complete_dataset.csv")


#hello world

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

