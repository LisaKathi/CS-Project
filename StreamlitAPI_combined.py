
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from urllib.parse import urlencode


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