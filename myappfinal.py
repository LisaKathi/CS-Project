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
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter
from sklearn.ensemble import RandomForestRegressor
from PIL import Image
import requests
from io import BytesIO
from urllib.parse import urlencode
from pyxlsb import open_workbook as open_xlsb
import requests
from datetime import datetime
import xlsxwriter


st.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            width: 300px;
        }
    </style>
    """,
    unsafe_allow_html=True )

def load_data():
    return pd.read_csv(r"C:\Users\noelb\Desktop\CS Projekt\cleaned_tow.csv")

def apply_filters(df, title_input, artist_name_input, min_year, max_year, selected_option, min_price, max_price, min_area, max_area, selected_materials):
  
    filtered_df = df.copy()

    if title_input:
        filtered_df = filtered_df[filtered_df['Title'].str.contains(title_input, case=False)]
    if artist_name_input:
        filtered_df = filtered_df[filtered_df['Artist Name'].str.contains(artist_name_input, case=False)]

    filtered_df['Creation Year'] = pd.to_numeric(df['Creation Year'], errors='coerce')
    filtered_df = filtered_df[(filtered_df["Creation Year"] >= min_year) & (filtered_df["Creation Year"] <= max_year)]
    
    if selected_option == "Posthumous":
        filtered_df = filtered_df[filtered_df['Posthumous Combined'].isin([1])]
    elif selected_option == "Prehumous":
        filtered_df = filtered_df[filtered_df['Posthumous Combined'].isin([0])]

    filtered_df['Sales Amount in USD'] = df['Sales Amount in USD'].astype(float)
    filtered_df = filtered_df[(filtered_df['Sales Amount in USD'] >= min_price) & (filtered_df['Sales Amount in USD'] <= max_price)]

    filtered_df['Act. Area'] = df['Act. Area'].astype(float)
    filtered_df = filtered_df[(filtered_df['Act. Area'] >= min_area) & (filtered_df['Act. Area'] <= max_area)]

    if selected_materials:
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
            'Other Specific Techniques or Materials': 10
        }
        selected_categories = [filter_options[option] for option in selected_materials]
        filtered_df = filtered_df[filtered_df["Material Category"].isin(selected_categories)]

    return filtered_df

#loading the image from our figma design
artimage = "/Users\noelb\Desktop\CS Projekt\figmaart.png"
picture = Image.open(artimage)

#display the image using a sidebar in the app
st.sidebar.image(picture, use_column_width=True)

#Defining differnt pages
#main page
def main():
    colleft, colright = st.columns([3,1])

    with colleft:
        st.title("Home")
        st.title("Art Valuation App")
        st.header('CS Project by Group 2.2')

    with colright:
        st.image("/Users\noelb\Desktop\CS Projekt\figmaart2.png")



#page1
def page1():
    st.title("Data Discovery")
    df = load_data()
    
    # The columns are given new names so that the table looks a little better. 
    names_new_columns = {'artist_name':'Artist Name','year_artist_born':'Birth year','age':'Age','length':'Length','width':'Width','title_of_work':'Title','height':'Height'
                         ,'year_of_work':'Creation Year','age_at_work':'Age of Artist at Creation','lower_est_USD':'Lower est. USD','upper_est_USD':'Upper est. USD',
                         'sold_in_USD':'Sales Amount in USD','Material_Category':'Material Category','act_area':'Act. Area','posthumous_combined':'Posthumous Combined'}
    df.rename(columns=names_new_columns, inplace= True) #The new names are implimented 
    
   
    
    #Filter structure
    filters = {
        "title_input": "",
        "artist_name_input": "",
        "min_year": df["Creation Year"].min(),
        "max_year": df["Creation Year"].max(),
        "min_price": df["Sales Amount in USD"].min(),
        "max_price": df["Sales Amount in USD"].max(),
        "min_area": df["Act. Area"].min(),
        "max_area": df["Act. Area"].max(),
        "selected_option": "Show all",
        "selected_materials": []
    }
    
    
    #search for title
    st.sidebar.header('Search for artworks by title')
    filters["title_input"] = st.sidebar.text_input("Please an artwork title (or part of the title):")
    if filters["title_input"]:
        df = df[df["Title"].str.contains(filters["title_input"], case=False)]
    else: df = df
    
    
    
    #search for artist
    st.sidebar.header('Search for artworks by artists')
    filters["artist_name_input"] = st.sidebar.text_input("Please enter an artist's name (or part of the name):")
    if filters["artist_name_input"]:
        df = df[df["Artist Name"].str.contains(filters["artist_name_input"], case=False)]
    else: df = df
    
    
    #filter by year
    st.sidebar.header('Filter for artworks by year')
    
    #define variables for filter; for the year filter we make sure everything is int since only whole years make sense here.
    df['Creation Year'] = pd.to_numeric(df['Creation Year'], errors='coerce')
    
    filters['min_year'] = int(filters['min_year'])
    filters['max_year'] = int(filters['max_year'])
    
    creation_year = df["Creation Year"]
    
    min_year_input = st.sidebar.text_input("Select minimum year:", key="min_year_input")
    if min_year_input == "":
        min_year_input = int(creation_year.min())
    else:
        min_year_input = int(min_year_input)
        
    max_year_input = st.sidebar.text_input("Select maximum year:", key="max_year_input")
    if max_year_input == "":
        max_year_input = int(creation_year.max())
    else:
        max_year_input = int(max_year_input)
    
    filters["min_year"], filters["max_year"] = st.sidebar.slider("Filter by year", 
                                    filters["min_year"], 
                                    filters["max_year"],
                                    (min_year_input, 
                                    max_year_input),
                                    step=1)
    
    df["Creation Year"] = creation_year
    df = df[(df["Creation Year"] >= filters["min_year"]) & (df["Creation Year"] <= filters['max_year'])]
    
    
    
    #filter by price
    st.sidebar.header("Filter for artworks by price")
    
    #define variables for filter
    sold_in_usd = df["Sales Amount in USD"]

    min_value_input = st.sidebar.text_input("Select minimum price in USD:", key="min_value_input")
    if min_value_input == "":
        min_value_input = float(sold_in_usd.min())
    else:
        min_value_input = float(min_value_input)

    max_value_input = st.sidebar.text_input("Select maximum price in USD:", key="max_value_input")
    if max_value_input == "":
        max_value_input = float(sold_in_usd.max())
    else:
        max_value_input = float(max_value_input)

    filters["min_price"], filters["max_price"]= st.sidebar.slider("Filter by price range (USD)", 
                                    filters["min_price"],
                                    filters["max_price"],
                                    (min_value_input,
                                    max_value_input),
                                    step=1000.0)

    df["Sales Amount in USD"] = sold_in_usd
    df = df[(df["Sales Amount in USD"] >= filters["min_price"]) & (df["Sales Amount in USD"] <= filters['max_price'])]



    #filter by size
    st.sidebar.header("Filter for artworks by size")
    
    #define variables for filter
    act_area = df["Act. Area"]

    min_area_input = st.sidebar.text_input("Select minimum volume in cm^3:", key="min_area_input")
    if min_area_input == "":
        min_area_input = float(act_area.min())
    else:
        min_area_input = float(min_area_input)

    max_area_input = st.sidebar.text_input("Select maximum volume in cm^3:", key="max_area_input")
    if max_area_input == "":
        max_area_input = float(act_area.max())
    else:
        max_area_input = float(max_area_input)

    filters["min_area"], filters["max_area"]= st.sidebar.slider("Filter by size range", 
                                    filters["min_area"],
                                    filters["max_area"],
                                    (min_area_input,
                                    max_area_input),
                                    step=1000.0)

    df["Act. Area"] = act_area
    df = df[(df["Act. Area"] >= filters["min_area"]) & (df["Act. Area"] <= filters["max_area"])]

    

    # Filter by time of sale
    st.sidebar.header("Filter for artworks by time of sale")
    # Check if there are results after applying previous filters
    if not df.empty:
        posthumous_values = df["Posthumous Combined"].unique()

        if 1 in posthumous_values and 0 not in posthumous_values:
            # If only 1 is present, show only "Posthumous" radio button
            filters["selected_option"] = "Posthumous"
            st.sidebar.info("Only 'Posthumous' artworks available.")
        elif 0 in posthumous_values and 1 not in posthumous_values:
            # If only 0 is present, show only "Prehumous" radio button
            filters["selected_option"] = "Prehumous"
            st.sidebar.info("Only 'Prehumous' artworks available.")
        else:
            # If both 0 and 1 are present, show all three radio buttons
            checkbox_options = ["Show all", "Prehumous", "Posthumous"]
            filters["selected_option"] = st.sidebar.radio("Filter pre- and posthumous artworks:", checkbox_options)
                    
            if filters["selected_option"] == "Posthumous":
                df = df[df["Posthumous Combined"].isin([1])]
            elif filters["selected_option"] == "Prehumous":
                df = df[df["Posthumous Combined"].isin([0])]
            elif filters["selected_option"] == "Show all":
                df = df[df["Posthumous Combined"].isin([0, 1])]
    else:
        # If no results, hide the radio buttons
        st.sidebar.warning("No results for previous filters.")

   
    # Filter by material category 
    st.sidebar.header('Filter for artworks by material category')
    
    #define filter options and match them with their category information
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
        'Other Specific Techniques or Materials': 10
    }
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
        df = df[df["Material Category"].isin(selected_categories)]



    #make a shortened version of the data frame and toggle to show shortened / full df
    df_short = df.loc[:, ["Artist Name", "Title", "Creation Year", "Sales Amount in USD"]].copy()

    
    toggle = st.checkbox("Show full table")

    st.write("Filtered Artworks")
    
    if toggle:
        st.write(df)
    else:
        st.write(df_short)
        
    num_artworks_size = df.shape[0]
    st.markdown(f"Number of Artworks in Selected Range: **{num_artworks_size}**")
    
    
    
    #create download button for exel file
    def to_excel(df):
        excel_file_path = "filtered_artworks.xlsx"
        with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            format1 = workbook.add_format({'num_format': '0.00'})
            worksheet.set_column('A:A', None, format1)
        return excel_file_path
    df_xlsx = to_excel(df)
    st.download_button(label= "📥 Download filtered artworks as XLSX",
                                 data=df_xlsx,
                                 file_name= "filtered_artworks.xlsx")
                             
     
    #create download button for csv file.
    #We include this here since the integrated csv download button at the top of the filtered df might not be intuitive and because it will only download the shortened df if toggle is inactive, whereas this button will always download the full.
    def to_csv(df):
        output = BytesIO()
        df.to_csv(output, index=False)
        processed_data = output.getvalue()
        return processed_data
    df_csv = to_csv(df)
    st.download_button(label="📥 Download filtered artworks as CSV",
                    data=df_csv,
                    file_name="filtered_artworks.csv") 




#page2 - Artwork Sales Prediction
def page2():
    st.title("Artwork Sales Prediction")
    

    def load_data():
        data = pd.read_csv(r"C:\Users\noelb\Desktop\CS Projekt\cleaned_tow.csv")
        return (data.dropna())

    # Calls upon the prediction model
    def load_model():
        filename = r"C:\Users\noelb\Desktop\CS Projekt\finalized_artworks_prediction.sav"
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
    birth_year_input = st.number_input('Artist birth year', min_value=0, max_value=2023, step=1)
    age_input = st.number_input('Age of the artist', min_value = 0, max_value = 120, step = 1)
    length_input = st.number_input('Length (in cm)', min_value=0.00, step= 0.001) #min value and steps are float 
    width_input = st.number_input('Width (in cm)', min_value=0.00, step= 0.001)
    height_input = st.number_input('Height (in cm)', min_value=0.00, step=0.001)
    creation_year_input = st.number_input('Creation Year', min_value=0, max_value=2023, step=1)
    age_at_creation_input = st.number_input('Age of Artist at Creation', min_value=0, max_value=120, step=1)
    lower_est_usd_input = st.number_input('Lower est. USD', min_value=0.00, step=0.01)
    upper_est_usd_input = st.number_input('Upper est. USD', min_value=0.00, step=0.01)
    material_category_input = st.selectbox('Material_Category', filter_options.values()) #Here we must specify that it is the values, otherwise the code will take the keys
    st.write(filter_options)
    act_area_input = length_input*width_input*height_input #The result of multiplying the three is act_area, the user does not need the act. area 
    posthumous_combined_input = st.selectbox('Posthumous Combined', [0, 1])
    artist_rank_input = st.number_input('Artist rank', min_value = 0 , step = 1)
    st.write("We have made a ranking of the popularity of the artists, in which rank 1 groups together the 10% most popular artists and rank 10 the 10% least popular. ")

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
    #streamlit title 
    st.title("Search for Artist and Artwork Information")
    st.subheader("Enter the Name of an Artist or the Title of an Artwork to discover more")

    #api stuff
    client_id = 'a3b3fb5b6856893b54e4'
    client_secret = '6a488c5093dcf0711d10202310a0b7c1'
    token_url = 'https://api.artsy.net/api/tokens/xapp_token'
    token_params = {
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_url, params=token_params)
    response_data = response.json()

    # Extract the authentication token, from chatgpt i couldn't figure out myself how to do this
    xapp_token = response_data['token']
    # source: chatgpt, didn't know how to implement with x-app token
    headers = {
        'X-Xapp-Token': xapp_token,
        'Accept': 'application/vnd.artsy-v2+json'
    }

    #function to get artist information by name
    def get_artist_info(artist_name):
        #api only works if you replace spaces with hyphens and is lowercase
        artist_id = artist_name.lower().replace(' ', '-')
    # artsy api get request
        artist_url = f'https://api.artsy.net/api/artists/{artist_id}'
        artist_response = requests.get(artist_url, headers=headers)
    
        #response has to == 200 (from api documentation)
        if artist_response.status_code == 200:  
            artist_data = artist_response.json()
            #checks if link and images are available in artsy api, else none
            if '_links' in artist_data and 'image' in artist_data['_links']:
                image_url = artist_data['_links']['image'] 
                return artist_data, image_url
            else:
                return artist_data, None
        else:
            return None

    #function to search for images by artwork title with google api 
    def search_by_artwork_title(query):
        api_key = "AIzaSyA5ZBUprEpXqi1_riSJd-TPm9ZIso2jjzM"
        engine_id = "23cad24530288430c" 
        search_query = f'{query} artwork'
        cse_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={engine_id}&q={search_query}&searchType=image"
    
        response = requests.get(cse_url)
        search_result = response.json().get('items', [])    
        return search_result

    #function to display results of searching by artwork title (google api)
    def display_results(search_result, query):
        if search_result:
            st.write(f"Image for artwork title '{query}' will be displayed here")
            image_url = search_result[1]['link'] #show only 1 result
            st.image(image_url, caption=f"Showing Result for your Query: \'{query}\'") 
        else:
            st.write(f"No results found for your query: '{query}'.")

    #function to search for artwork information with artsy api 
    def get_artwork_info(artwork_title):
        formatted_title = artwork_title.lower().replace(' ', '-')
        artwork_url = f'https://api.artsy.net/api/artworks?title={formatted_title}'
        artwork_response = requests.get(artwork_url, headers=headers)
     
        #check api response, if == 200 returns artwork data
        if artwork_response.status_code == 200:
            artwork_data = artwork_response.json()
            if '_embedded' in artwork_data and 'artworks' in artwork_data['_embedded']:
                return artwork_data['_embedded']['artworks']
            else:
                return []
        else:
            return []


    # function to calculate age with datetime
    def calculate_artist_age(birthdate, deathdate):
        if birthdate:
            birth_year = int(birthdate[:4])
            death_year = int(deathdate[:4]) if deathdate else datetime.now().year
            return death_year - birth_year
        else:
            return 'No birthdate or deathdate was found'

    user_query = st.text_input("Enter the Name of the Artist or the Artwork Title:")


    #buttons to trigger search for artist
    if st.button("Click to Search for an Artist"):
        if user_query:
            artist_info, image_url = get_artist_info(user_query) #call artist info
                
            if artist_info: #retrieve artist info, from api documentation
                birth_year = artist_info.get('birthday', '')[:4] if artist_info.get('birthday') else 'No Information available for birth year'
                death_year = artist_info.get('deathday', '')[:4] if artist_info.get('deathday') else 'No Information available for death year'
                age = calculate_artist_age(artist_info.get('birthday'), artist_info.get('deathday'))
                nationality = artist_info.get('nationality', '')
                hometown = artist_info.get('hometown', '')
                biography = artist_info.get('biography')

                st.subheader(f"Artist Details for {user_query}:") #added formatting with markdown
                st.markdown(f"**Birth Year**: {birth_year}")
                st.markdown(f"**Death Year**: {death_year}")
                st.markdown(f"**Age**: {age}")
                st.markdown(f"**Nationality**: {nationality}")
                st.markdown(f"**Hometown**: {hometown}")
                st.markdown(f"**Biography**:\n{biography}\n")

                #check if artsy api has info on artworks by artist and retrieve image, title and date
                if '_links' in artist_info and 'artworks' in artist_info['_links']:
                    artworks_link = artist_info['_links']['artworks']['href']
                    artworks_response = requests.get(artworks_link, headers=headers)
                
                    if artworks_response.status_code == 200: #api response, returns title and date of artwork
                        artworks_data = artworks_response.json()
                        st.markdown(f"**Some Artworks by {user_query}**: ")
                        for artwork in artworks_data['_embedded']['artworks']:
                            title = artwork['title']
                            date = artwork.get('date', 'Date not available')
                            st.write(f"- {title}, {date}")
                        
                            images = search_by_artwork_title(f'{user_query} {title}')  # search for images by artwork title function, repurposed to use info stored in artsy api 
                            if images:
                                image_url = images[0]['link']
                                st.image(image_url, caption=f"Image related to '{title}'", width=300) #made the artwork smaller, otherwise in the way
                            else:
                                st.write("No image found for this artwork.")
            else:
                st.write(f"No artist found with the name '{user_query}'.")


    if st.button("Click to Search for an Artwork"): #trigger search for artwork, now with artwork info
        if user_query:
            images = search_by_artwork_title(user_query) #search for image of artwork, with google api
            if images:
                image_url = images[0]['link']
                st.image(image_url, caption=f"Image related to '{user_query}'")
            else:
                st.write("No image found for this artwork.")
        
            formatted_query = user_query.lower().replace(' ', '-') #formatted so artsy api can uses query
            artwork_info = get_artwork_info(formatted_query)

            if artwork_info: 
                found_artworks = [artwork for artwork in artwork_info if artwork.get('title', '').lower() == user_query.lower()] #make sure artsy has the title of the artwork info

                if found_artworks:
                    found_artwork = found_artworks[0]  # showing only the first found artwork
                    title = found_artwork.get('title', 'Title not available') #return info 
                    date = found_artwork.get('date', 'Date not available')
                    medium = found_artwork.get('medium', 'Medium not available')
                    artist_name = found_artwork.get('_embedded', {}).get('artists', [{}])[0].get('name', 'Artist Name Not Found')
                    category = found_artwork.get('category', 'Category not available')            

                    st.subheader(f"Artwork Details for '{user_query}':") #formatting with markdown
                    st.markdown(f"**Title**: {title}")
                    st.markdown(f"**Date**: {date}")
                    st.markdown(f"**Artist Name**: {artist_name}")
                    st.markdown(f"**Category**: {category}")
                    st.markdown(f"**Medium**: {medium}")
        
                else:
                    st.write(f"No artwork details found for '{user_query}'.")
            else:
                st.write(f"No artwork details found for '{user_query}'.")
            

    if st.button("Click to Reset"):
        user_query = ""  # added to empty the user_query variabl, clears the text input field

#page4 - Vizualisation
def page4():
    st.title('Visualisation')

    # Load the CSV file into a DataFrame
    df = pd.read_csv(r"C:\Users\noelb\Desktop\CS Projekt\cleaned_tow.csv")

    # Multicheck options for selecting plots
    selected_plots = st.multiselect('Select plots to display',['Scatterplot for any Artist', 'Line Plot After 1900', 'Line Plot Before 1900','Distribution by material category','Number of Unique Artist Names per Century'])

    # Display selected plots
    for plot in selected_plots:
        if plot == 'Scatterplot for any Artist':
            # User input for artist name
            artist_name_input = st.text_input('Enter artist name')

            # Filter the DataFrame based on the entered artist name
            artist_name_filtered_df = df[df['artist_name'] == artist_name_input]

            # Check if there are enough data points to create a Scatterplot
            if len(artist_name_filtered_df) > 1:
                # Set a stylistic theme for Seaborn
                sns.set(style="whitegrid")

                # Create the Seaborn Scatterplot with color variations
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.scatterplot(x='year_of_work', y='sold_in_USD', data=artist_name_filtered_df, hue='sold_in_USD', size='sold_in_USD', sizes=(50, 200), palette='viridis', ax=ax)

                # Add title and axis labels
                ax.set_title('Sales Values for ' + artist_name_input + ' Artworks Over the Years', fontsize=16)
                ax.set_xlabel('Year of Work', fontsize=14)
                ax.set_ylabel('Sale Value in USD (in millions)', fontsize=14)

                # Display Y-axis labels in millions format
                formatter = FuncFormatter(lambda x, _: f'{int(x / 1e6)}M')
                ax.yaxis.set_major_formatter(formatter)

                # Add legend
                ax.legend(title='Sale Value', title_fontsize='14', fontsize='12', loc='upper right')

                # Beautify the plot
                sns.despine(left=True, bottom=True)

                # Show the plot in Streamlit
                st.pyplot(fig)
            else:
                st.text("There is not enough data for the artist " + artist_name_input + " create a Scatterplot.")

        elif plot == 'Line Plot After 1900':
            # Convert 'year_of_work' to numeric, filtering data after 1900
            df['year_of_work'] = pd.to_numeric(df['year_of_work'], errors='coerce')
            df = df[df['year_of_work'] > 1900]

            # Create a line plot
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(x='year_of_work', y='sold_in_USD', data=df, marker='o', ax=ax)

            # Add title and axis labels
            ax.set_title('Price of the Work Over Year of Work (After 1900)')
            ax.set_xlabel('Year of Work')
            ax.set_ylabel('Sale Value in Million USD')

            # Show the plot in Streamlit
            st.pyplot(fig)

        elif plot == 'Line Plot Before 1900':
            df = pd.read_csv(r"C:\Users\noelb\Desktop\CS Projekt\cleaned_tow.csv")
            df['year_of_work'] = pd.to_numeric(df['year_of_work'], errors='coerce')
            df = df[df['year_of_work'] < 1900]

            # Create a line plot
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(x='year_of_work', y='sold_in_USD', data=df, marker='o', ax=ax)

            # Add title and axis labels
            ax.set_title('Price of the Work Over Year of Work (Before 1900)')
            ax.set_xlabel('Year of Work')
            ax.set_ylabel('Sale Value in Million USD')

            # Show the plot in Streamlit
            st.pyplot(fig)
        
        elif plot == 'Distribution by material category':
            # Count the number of different material categories
            material_counts = df['Material_Category'].value_counts()

            # Create a bar plot with Seaborn
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=material_counts.index, y=material_counts.values, ax=ax)

            # Add labels and title
            ax.set_title('Number of Different Material Categories')
            ax.set_xlabel('Material Category')
            ax.set_ylabel('Count')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=0, ha='center')

            # Display the plot in Streamlit
            st.pyplot(fig)
            st.write("""
            1. Paints and Pigments
            2. Metals and Sculpting Materials
            3. Printmaking and Graphic Arts
            4. Drawing and Writing Tools
            5. Mixed Media and Miscellaneous
            6. Traditional and Specialized Techniques
            7. Photography and Digital Art
            8. Sculpting and Carving
            9. Unconventional and Unique Techniques
            10. Other Specific Techniques or Materials
            """)
            
        elif plot == 'Number of Unique Artist Names per Century':
            # Extract the century from the 'year_artist_born' column
            df['century'] = (df['year_artist_born'] // 100) + 1

            # Count the number of unique artist names per century
            century_counts = df.groupby('century')['artist_name'].nunique()

            # Create a bar plot with Seaborn
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=century_counts.index, y=century_counts.values, ax=ax)

            # Add labels and title
            ax.set_title('Number of Unique Artist Names per Century')
            ax.set_xlabel('Century')
            ax.set_ylabel('Number of Artists')

            # Show the plot in Streamlit
            st.pyplot(fig) 

        
#reduced total lines of code, removed __main__ = __name__ line and removed except error line and combined search by artist name and title of work -iole
#also edited the messages displayed to user on streamlit
    
pages = {
    "Home": main,
    "Data Discovery": page1,
    "Artwork Sales Prediction": page2,
    "Search by Artwork or Artist": page3,
    "Visualisation" : page4
}

selection = st.sidebar.radio("Go to", list(pages.keys()))

st.sidebar.markdown("---")

# Zeige die ausgewählte Seite an
pages[selection]()
