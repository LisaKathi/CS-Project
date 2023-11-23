import streamlit as st
import pandas as pd

st.title("Art Valuation App")
st.header('CS Project by Group 2.2')
df = pd.read_csv(r"C:\Users\ioles\Downloads\AppraiSet_complete_dataset.csv")
st.write(df.head(10))
###please don't edit anything before this line #####

st.write("Displaying DataFrame:")
st.dataframe(df)
st.sidebar.title('Sort options')
st.button('Hit me')
slider_value = st.sidebar.slider("Slider Label", 0, 100, 50)

checkbox_value = st.sidebar.checkbox("Checkbox Label")
