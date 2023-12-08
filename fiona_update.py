#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 20:53:07 2023

@author: fiona
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle 
from sklearn.ensemble import RandomForestRegressor
from PIL import Image
import requests
from io import BytesIO
from urllib.parse import urlencode

st.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            width: 300px;
        }
    </style>
    """,
    unsafe_allow_html=True
)



#Defining differnt pages
#main page
def main():
    st.title("Home")
    st.title("Art Valuation App \U0001F3A8")
    st.header('CS Project by Group 2.2')




#page1 - Data Discovery
def page1():
    st.title("Data Discovery") 
    df = pd.read_csv("/Users/fiona/Documents/CS-Project/cleaned_tow.csv")

    # The columns are given new names so that the table looks a little better. 
    names_new_columns = {'artist_name':'Artist Name','year_artist_born':'Birth year','age':'Age','length':'Length','width':'Width','title_of_work':'Title','height':'Height'
                         ,'year_of_work':'Creation Year','age_at_work':'Age of Artist at Creation','lower_est_USD':'Lower est. USD','upper_est_USD':'Upper est. USD',
                         'sold_in_USD':'Sales Amount in USD','Material_Category':'Material Category','act_area':'Act. Area','posthumous_combined':'Posthumous Combined'}
    df.rename(columns=names_new_columns, inplace= True) #The new names are implimented 
    filtered_df = df

    
    #search for title
    st.sidebar.header('Search for artworks by title')
    title_input = st.sidebar.text_input("Please an artwork title (or part of the title):")
    if title_input:
        filtered_df = filtered_df[filtered_df['Title'].str.contains(title_input, case=False)]
    else: filtered_df = filtered_df
    
    
    
    # search for artist
    st.sidebar.header('Search for artworks by artists')
    artist_name_input = st.sidebar.text_input("Please enter an artist's name (or part of the name):")
    if artist_name_input:
        filtered_df = filtered_df[filtered_df['Artist Name'].str.contains(artist_name_input, case=False)]
    else: filtered_df = filtered_df



    #filter by year
    #we need to convert Creation Year to numeric, because otherwise compares int with string####
    st.sidebar.header('Filter for artworks by year')
    df['Creation Year'] = pd.to_numeric(df['Creation Year'], errors='coerce')
    
    creation_year = df["Creation Year"]
   
    min_year_input = st.sidebar.text_input("Select minimum year:", key="min_year_input")
    if min_year_input == "":
        min_year_input = int(df['Creation Year'].min()) if not pd.isnull(df['Creation Year']).all() else 0
    else:
        min_year_input = int(min_year_input)
        
    max_year_input = st.sidebar.text_input("Select maximum year:", key="max_year_input")
    if max_year_input == "":
        max_year_input = int(df['Creation Year'].max()) if not pd.isnull(df['Creation Year']).all() else 0
    else:
        max_year_input = int(max_year_input)
    
    min_year, max_year = st.sidebar.slider("Filter by year", 
                                    int(df['Creation Year'].min()) if not pd.isnull(df['Creation Year']).all() else 0, 
                                    int(df['Creation Year'].max()) if not pd.isnull(df['Creation Year']).all() else 0,
                                    (min_year_input,
                                    max_year_input),
                                    step=1)
    
    df["Creation Year"] = creation_year
    filtered_df = filtered_df[(filtered_df["Creation Year"] >= min_year) & (filtered_df["Creation Year"] <= max_year)]
    
    
    
    # Filter by time of sale
    st.sidebar.header("Filter for artworks by time of sale")
    # radio buttons to filter all/posthumous/prehumous artworks
    checkbox_options = ["Show all", "Prehumous", "Posthumous"]
    selected_option = st.sidebar.radio("Filter pre- and posthumous artworks:", checkbox_options)
    
    if selected_option == "Posthumous": # only true is considered posthumous
        filtered_df = filtered_df[filtered_df['Posthumous Combined'].isin([1])]
    elif selected_option == "Prehumous":
        filtered_df = filtered_df[filtered_df['Posthumous Combined'].isin([0])]
    elif selected_option == "Show all":
        filtered_df = filtered_df[filtered_df['Posthumous Combined'].isin([0,1])]


    
    #filter by price
    st.sidebar.header("Filter for artworks by price")
    
    # extract Sales Amount in USD column, remove unnecessary caracters, and convert to float
    sold_in_usd = df['Sales Amount in USD']

    min_value_input = st.sidebar.text_input("Select minimum price:", key="min_value_input")
    if min_value_input == "":
        min_value_input = float(0)
    else:
        min_value_input = float(min_value_input)

    max_value_input = st.sidebar.text_input("Select maximum price:", key="max_value_input")
    if max_value_input == "":
        max_value_input = float(sold_in_usd.max())
    else:
        max_value_input = float(max_value_input)  

    min_price, max_price = st.sidebar.slider("Filter by price range", 
                                    float(0), 
                                    float(sold_in_usd.max()),
                                    (min_value_input,
                                    max_value_input),
                                    step=(float(1000)))

    filtered_df['Sales Amount in USD'] = sold_in_usd
    filtered_df = filtered_df[(filtered_df['Sales Amount in USD'] >= min_price) & (filtered_df['Sales Amount in USD'] <= max_price)]



    # filter by size
    st.sidebar.header('Filter for artworks by size')

    # extract this column from the dataframe 
    act_area = df['Act. Area']

    min_area_input = st.sidebar.text_input("Select minimum area:", key="min_area_input")
    if min_area_input == "":
        min_area_input = float(act_area.min())
    else:
        min_area_input = float(min_area_input)  # Umwandlung in eine Dezimalzahl

    max_area_input = st.sidebar.text_input("Select maximum area:", key="max_area_input")
    if max_area_input == "":
        max_area_input = float(act_area.max())
    else:
        max_area_input = float(max_area_input)  # Umwandlung in eine Dezimalzahl

    # Slider to filter based on Act. Area, selected min_area, max_area and default values myself so all is int.
    min_area, max_area = st.sidebar.slider("Filter by size range",
                                           float(act_area.min()),
                                           float(act_area.max()),
                                           (min_area_input,
                                           max_area_input),
                                           step=(float(1000)))

    filtered_df['Act. Area'] = act_area
    filtered_df = filtered_df[(filtered_df['Act. Area'] >= min_area) & (filtered_df['Act. Area'] <= max_area)]



    # filter by Material Category 
    st.sidebar.header('Filter for artworks by material category')

    filter_options = {
        'Paints and Pigments': 1,
        'Metals and Sculpting Materials': 2,
        'Printmaking and Graphic Arts': 3,
        'Drawing and Writing Tools': 4,
        'Mixed Media and Miscellaneous': 5,
        'Traditional and Specialized Techniques': 6,
        'Photography and Digital Art': 7,
        'Sculpting and Carving': 8,
        'Unconventional and Unique Techniques': 9,
        'Other Specific Techniques or Materials': 10 }

    categories = {
        'Paints and Pigments': 'This category contains artworks made of oil, acrylic, spray, pastel, tempera, watercolor, watercolour, pigment, color.',
        'Metals and Sculpting Materials': 'This category contains artworks made of bronze, gold, patinated, wrought, alabaster, polished, copper, stainless, wood, cast, silver, steel, aluminum, walnut, plumbago, stone, corten, metallised, lead, burnished, brass, earthenware.',
        'Printmaking and Graphic Arts': 'This category contains artworks made of cprint, offset, charcoal, screenprint, letterpress, etching.',
        'Drawing and Writing Tools': 'This category contains artworks made of ballpoint, pen, signed, crayon, pencil, conte, marker, felttip.',
        'Mixed Media and Miscellaneous': 'This category contains artworks made of embroidery, synthetic, variable, mixed, ikb, paper, painted, polymer, glazed, alkyd, resin, polyuréthane, household, digital, book, fabric, gelatin, sump, vinyl, polyester, dye, offsetlithographin, monoprint, gypsum, printed, vegetable, archival, wool, digitally, enamel, monotype, cardboard, roll, woodcut, cement, lacquer, mirrored, oilstick, collage, pva, metal, bamboo, wires, wire, sand, epson, ektacolor, unframed, peacock, plastic, flashe, water, oxidation, porcelain, molave, handknitted, embossed, handembellished, polystone, silk, vacuumformed, cobblestones, feathers, diasecmounted, ukiyoe, giclee, giclée, handpainted, homemade, cotton, duratran, indian, varnished, handcut, fibreglass, vintage, humbrol.',
        'Traditional and Specialized Techniques': 'This category contains artworks made of silkscreen, encaustic, terracotta, leather, screen, lambda, glass.',
        'Photography and Digital Art': 'This category contains artworks made of ilfochrome, chromogenic, ink, cibachrome, photogram, inkjet, stencil, tar, photographic, epoxy, plaster.',
        'Sculpting and Carving': 'This category contains artworks made of graphite, wax, chalk.',
        'Unconventional and Unique Techniques': 'This category contains artworks made of language, led, electronic, neon, kinetic.',
        'Other Specific Techniques or Materials': 'This category contains artworks made of Other Specific Techniques or Materials: Any material that doesn\'t fit neatly into the above categories.' }

    selected_materials = []

    # checkboxess
    for option, info in filter_options.items():
        checkbox_state = st.sidebar.checkbox(option)
        
        with st.sidebar.expander("Info"):
             st.write(categories.get(option))
             
        if checkbox_state:
            selected_materials.append(option)
            
    if selected_materials:
        selected_categories = [filter_options[option] for option in selected_materials]
        filtered_df = filtered_df[filtered_df["Material Category"].isin(selected_categories)]

                   


    #make a shoetenes version of the data frame and toggle
    df_short = filtered_df.loc[:, ["Artist Name", "Title", "Creation Year", "Sales Amount in USD"]].copy()

    import  streamlit_toggle as tog

    toggle = tog.st_toggle_switch(label="Show full table", 
              key="Key1", 
              default_value=False, 
              label_after = False, 
              inactive_color = '#D3D3D3', 
              active_color="#11567f", 
              track_color="#29B5E8"
                  )

    st.write("Filtered Artworks")
    
    if toggle:
        st.write(filtered_df)
    else:
        st.write(df_short)
        
    num_artworks_size = filtered_df.shape[0]
    st.markdown(f"Number of Artworks in Selected Range: **{num_artworks_size}**")






#page2 - Artwork Sales Prediction
def page2():
    st.title("Artwork Sales Prediction")
    

    def load_data():
        data = pd.read_csv("/Users/fiona/Documents/CS-Project/My first appprosper_data_app_dev.csv")
        return (data.dropna())

    # Calls upon the prediction model
    def load_model():
        filename = r"C:\Users\loren\OneDrive\Documents\5 Semester\CS\Groupe project\finalized_artworks_prediction.sav"
        loaded_model = pickle.load(open(filename, "rb"))
        return (loaded_model)

    # Load Data and Model 
    data = load_data()
    model = load_model()

    filter_options = {
        'Paints and Pigments': 1,
        'Metals and Sculpting Materials': 2,
        'Printmaking and Graphic Arts': 3,
        'Drawing and Writing Tools': 4,
        'Mixed Media and Miscellaneous': 5,
        'Traditional and Specialized Techniques': 6,
        'Photography and Digital Art': 7,
        'Sculpting and Carving': 8,
        'Unconventional and Unique Techniques': 9,
        'Other Specific Techniques or Materials': 10 }

    st.write('Enter the following details about your artwork please')
    # User inputs of his artwork 
    birth_year_input = st.number_input('Birth year', min_value=0, max_value=2023, step=1)
    age_input = st.number_input('Age', min_value = 0, max_value = 120, step = 1)
    length_input = st.number_input('Length', min_value=0.00, step= 0.001) #min value and steps are float 
    width_input = st.number_input('Width', min_value=0.00, step= 0.001)
    height_input = st.number_input('Height', min_value=0.00, step=0.001)
    creation_year_input = st.number_input('Creation Year', min_value=0, max_value=2023, step=1)
    age_at_creation_input = st.number_input('Age of Artist at Creation', min_value=0, max_value=120, step=1)
    lower_est_usd_input = st.number_input('Lower est. USD', min_value=0.00, step=0.01)
    upper_est_usd_input = st.number_input('Upper est. USD', min_value=0.00, step=0.01)
    material_category_input = st.selectbox('Material_Category', filter_options.values()) #Here we must specify that it is the values, otherwise the code will take the keys
    act_area_input = length_input*width_input*height_input #The result of multiplying the three is act_area, the user does not need the act. area 
    posthumous_combined_input = st.selectbox('Posthumous Combined', [0, 1])
    artist_rank_input = st.number_input('Artist rank', min_value = 0 , step = 1)

    # Combine user inputs into a DataFrame for prediction
    user_input_df = pd.DataFrame({
        'year_artist_born': [birth_year_input],
        'age' : [age_input],
        'length': [length_input],
        'width': [width_input],
        'height': [height_input],
        'year_of_work': [creation_year_input],
        'age_at_work': [age_at_creation_input],
        'lower_est_USD': [lower_est_usd_input],
        'upper_est_USD': [upper_est_usd_input],
        'Material_Category': [material_category_input],
        'act_area' : [act_area_input],
        'posthumous_combined': [posthumous_combined_input],
        'artist_rank' : [artist_rank_input] })

    #The input data is run through our prediction model 
    input_prediction = model.predict(user_input_df)
    st.write(f'The result of the prediction is as follows:', input_prediction)






#page3 - Search
def page3():
    st.title("Search by Artwork or Artist")
    

    def search_image(query):
        api_key = "AIzaSyA5ZBUprEpXqi1_riSJd-TPm9ZIso2jjzM"
        engine_id = "23cad24530288430c" 

        search_query_combined = f'{query} artwork or {query} artist'
    

        cse_url_combined = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={engine_id}&q={search_query_combined}&searchType=image"
    
        response_combined = requests.get(cse_url_combined)

        search_results_combined = response_combined.json().get('items', [])
 

        display_results(search_results_combined, query)

    #edited to display only 1 image and display combined search by artist / artwork title


    def display_results(search_results, query):
        if search_results:
            st.write(f"Search results for '{query}':")
            image_url = search_results[0]['link']  #display only the first image found
            st.image(image_url, caption=f"Showing the Top Result for your Query: {query}", use_column_width=True)
            st.markdown("---")  # image spacing
        else:
            st.write(f"No results found for your query: '{query}'.")

    def search_function():
        st.header('Search by Artist or Name of the Artwork \U0001F3A8 ')
        query = st.text_input("Please enter the Name of the Artist or Artwork Title:", "")
    
        if query:
            search_image(query)


    search_function() # start the streamlit by calling the function

#reduced total lines of code, removed __main__ = __name__ line and removed except error line and combined search by artist name and title of work -iole
#also edited the messages displayed to user on streamlit
    




pages = {
    "Home": main,
    "Data Discovery": page1,
    "Artwork Sales Prediction": page2,
    "Search by Artwork or Artist": page3
}

selection = st.sidebar.radio("Go to", list(pages.keys()))

st.sidebar.markdown("---")

# Zeige die ausgewählte Seite an
pages[selection]()

