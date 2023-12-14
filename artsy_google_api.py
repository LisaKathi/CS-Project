
###2 api for search for artworks and artist info#####

import streamlit as st
import requests
from datetime import datetime

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
                artist_name = found_artwork.get('_embedded', {}).get('artists', [{}])[0].get('name', 'Artist Name Not Available')
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
