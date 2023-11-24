import streamlit as st
import pandas as pd
import numpy as np

st.title("Art Valuation App \U0001F3A8")
st.header('CS Project by Group 2.2')
df = pd.read_csv(r"C:\Users\Björn Blumer\Downloads\AppraiSet_complete_dataset.csv")

# checkbox to filter posthumous artworks
posthumous_checkbox = st.checkbox("Filter Posthumous Artworks")

# extract sold_in_USD column, remove unnecessary caracters, and convert to float
sold_in_usd = df['sold_in_USD'].str.replace('$', '').str.replace(',', '').astype(float)

# slider to filter based on sold_in_USD
min_price, max_price = st.slider("Filter by Price Range", 
                                min_value=float(sold_in_usd.min()),
                                max_value=float(sold_in_usd.max()),
                                value=(float(0), float(sold_in_usd.max())))

# filter the dataframe based on the checkbox and slider values
filtered_df = df.copy()

if posthumous_checkbox:
    # only true is considered posthumous
    filtered_df = filtered_df[filtered_df['posthumous_T_or_F_or_U'].isin(['True'])]

filtered_df['sold_in_USD'] = sold_in_usd
filtered_df = filtered_df[(filtered_df['sold_in_USD'] >= min_price) & (filtered_df['sold_in_USD'] <= max_price)]

# Display the dataframe
st.write("Filtered Artworks:")
st.table(filtered_df)



