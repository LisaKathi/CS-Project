import streamlit as st
import requests
from IPython.display import Image, display
from datetime import datetime
st.title("Artist and Artwork Info")
st.subheader("Search by Artist name to return Information on Artist or search by Artwork Title to return an Image of the Artwork")
#first we define a function to calculate age, with birthdate & deathdates)
def calculate_artist_age(birthdate, deathdate):
    if birthdate:
        birth_year = int(birthdate[:4])
        death_year = int(deathdate[:4]) if deathdate else datetime.now().year
        return death_year - birth_year
    return 'No birthdate or deathdate was found'
#added slicing with [:4]
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
# Define headers for API requests
headers = {
    'X-Xapp-Token': xapp_token,
    'Accept': 'application/vnd.artsy-v2+json'
}
# create fnction to get artist information by name
def get_artist_info(artist_name):
    #api only works if you replace spaces with hyphens
    artist_id = artist_name.lower().replace(' ', '-')
# artsy api get request
    artist_url = f'https://api.artsy.net/api/artists/{artist_id}'
    artist_response = requests.get(artist_url, headers=headers)
    #to check if the request was successful, otherwise return none
    
    #Errors:  (from api documentation)
    # HTTP status codes are used to indicate success or failure of a request.
    # 200 OK - Request succeeded.
    if artist_response.status_code == 200:  
        artist_data = artist_response.json()
        if '_links' in artist_data and 'image' in artist_data['_links']:
            image_url = artist_data['_links']['image']['href']
            return artist_data, image_url
        else:
            return artist_data, None
    else:
        return None, None

def search_by_artwork_title(query, search_by):
    api_key = "AIzaSyA5ZBUprEpXqi1_riSJd-TPm9ZIso2jjzM"
    engine_id = "23cad24530288430c" 
    if search_by == "Artist Name":
        search_query = f'{query} artist'
    else:
        search_query = f'{query} artwork'
    cse_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={engine_id}&q={search_query}&searchType=image"
    
    response = requests.get(cse_url)
    search_result = response.json().get('items', [])
            
    return search_result
def display_results(search_result, query):
    if search_result:
        st.write(f"Image for artwork title '{query}' will be displayed here")
        image_url = search_result[0]['link']
        st.image(image_url, caption=f"Showing Result for your Query: {query}", use_column_width=True)
    else:
        st.write(f"No results found for your query: '{query}'.")


search_by = st.selectbox("Search by:", ["Artist Name", "Artwork Title"])
user_query = st.text_input("Enter your search query:")
#found parameters on the artsy api "artists"
if st.button("Click to Search"):
    if user_query:
        if search_by == "Artwork Title": 
            search_result = search_by_artwork_title(user_query, search_by)
            display_results(search_result, user_query)
        elif search_by == "Artist Name":
            artist_info, image_url = get_artist_info(user_query)
            
            # Retrieve image from the provided href URL
            if '_links' in artist_info and 'image' in artist_info['_links']:
                image_href = artist_info['_links']['image']['href']
                image_version = 'large'  # You can select the desired image version from the available options
        # Replace {image_version} with the desired image version
                image_href = image_href.format(image_version=image_version)
                st.image(image_href, caption="Displaying Image related to Artist", width=300)
            else:
                st.write("Image not available.")
            if artist_info:
                
                #access artist info, get requests
                birth_year = artist_info.get('birthday', '')[:4] if artist_info.get('birthday') else 'No Information available for birth year'
                death_year = artist_info.get('deathday', '')[:4] if artist_info.get('deathday') else 'No Information available for death year'
                age = calculate_artist_age(artist_info.get('birthday'), artist_info.get('deathday'))
                nationality = artist_info.get('nationality', '')
                hometown = artist_info.get('hometown', '')
                biography = artist_info.get('biography')

                #write in streamlit 
                st.write(f"\nArtist Details for {user_query}:\n")
                st.write(f"Birth Year: {birth_year}")
                st.write(f"Death Year: {death_year}")
                st.write(f"Age: {age}")
                st.write(f"Nationality: {nationality}")
                st.write(f"Hometown: {hometown}")
                st.write(f"Biography:\n{biography}\n")