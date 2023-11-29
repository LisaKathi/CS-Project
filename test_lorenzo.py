import streamlit as st
import pandas as pd
import numpy as np
import pickle 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer

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
    (df['Creation Year'] <= selected_years[1])]

st.write("Filtered Artworks by Year:")
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
st.write("Filtered Artworks by Price:")
st.write(filtered_2_df)

# Counter for the number of artworks in the selected range
num_artworks_price = filtered_2_df.shape[0]
st.markdown(f"Number of Artworks in Selected Range: **{num_artworks_price}**")



#Slider for size of the work (area column)
st.header('Filter for artworks by Size')

# extract Act. Area
act_area = df['Act. Area']

# slider to filter based on Act. Area
min_area, max_area = st.slider("Filter by Size Range", 
                                min_value=float(act_area.min()),
                                max_value=float(act_area.max()),
                                value=(float(0), float(act_area.max())))

# filter the dataframe based on the checkbox and slider values
filtered_3_df = df.copy()

filtered_3_df['Act. Area'] = act_area
filtered_3_df = filtered_3_df[(filtered_3_df['Act. Area'] >= min_area) & (filtered_3_df['Act. Area'] <= max_area)]

# Display the dataframe
st.write("Filtered Artworks by Size:")
st.write(filtered_3_df)

# Counter for the number of artworks in the selected range
num_artworks_size = filtered_3_df.shape[0]
st.markdown(f"Number of Artworks in Selected Range: **{num_artworks_size}**")



#Multi-checkbox, Filter by Material Category (used ChatGPT)
st.header('Filter for artworks by Material Category')

# Define the filter options
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


# Multicheckbox for filtering based on categories
selected_categories = st.multiselect("Select Material Category", filter_options.keys())


# Checkbox for showing more information
# Information about categories
categories = {
    'Paints and Pigments': ['This category contains artworks made of','oil', 'acrylic', 'spray', 'pastel', 'tempera', 'watercolor', 'watercolour', 'pigment', 'color'],
    'Metals and Sculpting Materials' : ['This category contains artworks made of','bronze', 'gold', 'patinated', 'wrought', 'alabaster', 'polished', 'copper', 'stainless', 'wood', 'cast', 'silver', 'steel', 'aluminum', 'walnut', 'plumbago', 'stone', 'corten', 'metallised', 'lead', 'burnished', 'brass', 'earthenware'],
    'Printmaking and Graphic Arts': ['This category contains artworks made of','cprint', 'offset', 'charcoal', 'screenprint', 'letterpress', 'etching'],
    'Drawing and Writing Tools': ['This category contains artworks made of','ballpoint', 'pen', 'signed', 'crayon', 'pencil', 'conte', 'marker', 'felttip'],
    'Mixed Media and Miscellaneous': ['This category contains artworks made of','embroidery', 'synthetic', 'variable', 'mixed', 'ikb', 'paper', 'painted', 'polymer', 'glazed', 'alkyd', 'resin', 'polyuréthane', 'household', 'digital', 'book', 'fabric', 'gelatin', 'sump', 'vinyl', 'polyester', 'dye', 'offsetlithographin', 'monoprint', 'gypsum', 'printed', 'vegetable', 'archival', 'wool', 'digitally', 'enamel', 'monotype', 'cardboard', 'roll', 'woodcut', 'cement', 'lacquer', 'mirrored', 'oilstick', 'collage', 'pva', 'metal', 'bamboo', 'wires', 'wire', 'sand', 'epson', 'ektacolor', 'unframed', 'peacock', 'plastic', 'flashe', 'water', 'oxidation', 'porcelain', 'molave', 'handknitted', 'embossed', 'handembellished', 'polystone', 'silk', 'vacuumformed', 'cobblestones', 'feathers', 'diasecmounted', 'ukiyoe', 'giclee', 'giclée', 'handpainted', 'homemade', 'cotton', 'duratran', 'indian', 'varnished', 'handcut', 'fibreglass', 'vintage', 'humbrol'],
    'Traditional and Specialized Techniques': ['This category contains artworks made of','silkscreen', 'encaustic', 'terracotta', 'leather', 'screen', 'lambda', 'glass'],
    'Photography and Digital Art': ['This category contains artworks made of','ilfochrome', 'chromogenic', 'ink', 'cibachrome', 'photogram', 'inkjet', 'stencil', 'tar', 'photographic', 'epoxy', 'plaster'],
    'Sculpting and Carving': ['This category contains artworks made of','graphite', 'wax', 'chalk'],
    'Unconventional and Unique Techniques': ['This category contains artworks made of','language', 'led', 'electronic', 'neon', 'kinetic'],
    'Other Specific Techniques or Materials': ['This category contains artworks made of','Other Specific Techniques or Materials: Any material that doesnt fit neatly into the above categories']
}
# Checkbox for showing more information
show_more_info = st.checkbox("Show More Information")

# Display more information for selected categories if the checkbox is selected
if show_more_info:
    st.write("Select Categories for More Information:")
    selected_info_categories = st.multiselect("Select Categories", categories)

    # Display additional information for the selected categories
    for category_id in selected_info_categories:
        st.write(f"Additional Information for Category {category_id}:")
        st.write(categories.get(category_id, "No information available"))



# Map selected categories to their corresponding values
selected_values = [filter_options[category] for category in selected_categories]

# Filter the DataFrame based on selected values
filtered_4_df = df[df['Material Category'].isin(selected_values)]

# Display the filtered DataFrame
st.write("Filtered Artworks by Material Category:")
st.write(filtered_4_df)

# Counter for the number of artworks in the selected range
num_artworks_material = filtered_4_df.shape[0]
st.markdown(f"Number of Artworks in Selected Range: **{num_artworks_material}**")




###Section 2 for making predictions 

st.title('Artwork Sales Prediction App')
def load_data():
    data = pd.read_csv(r"C:\Users\loren\OneDrive\Documents\5 Semester\CS\Groupe project\cleaned_tow.csv")
    return data

def load_model():
    filename = "final prediction.sav"
    loaded_model = pickle.load(open(filename, "rb"))
    return loaded_model 

data = load_data()
model = load_model() 


# User input
artist_name_input = st.text_input('Artist Name')
birth_year_input = st.number_input('Birth Year', min_value=0, max_value=2023, step=1)
age_input = st.number_input('Age', min_value=0, max_value=120, step=1)
length_input = st.number_input('Length', min_value=0.00, step= 0.001)
width_input = st.number_input('Width', min_value=0.00, step= 0.001)
title_input = st.text_input('Title')
height_input = st.number_input('Height', min_value=0.00, step=0.001)
creation_year_input = st.number_input('Creation Year', min_value=1000, max_value=2023, step=1)
age_at_creation_input = st.number_input('Age of Artist at Creation', min_value=0, max_value=120, step=1)
lower_est_usd_input = st.number_input('Lower Est. USD', min_value=0.00, step=0.01)
upper_est_usd_input = st.number_input('Upper Est. USD', min_value=0.00, step=0.01)
material_category_input = st.selectbox('Material Category', filter_options)
act_area_input = st.selectbox('Act. Area', df['Act. Area'].unique())
posthumous_combined_input = st.selectbox('Posthumous Combined', [0, 1])

# Combine user inputs into a DataFrame for prediction
user_input_df = pd.DataFrame({
    'Artist Name': [artist_name_input],
    'Birth Year': [birth_year_input],
    'Age': [age_input],
    'Length': [length_input],
    'Width': [width_input],
    'Title': [title_input],
    'Height': [height_input],
    'Creation Year': [creation_year_input],
    'Age of Artist at Creation': [age_at_creation_input],
    'Lower Est. USD': [lower_est_usd_input],
    'Upper Est. USD': [upper_est_usd_input],
    'Material Category': [material_category_input],
    'Act. Area': [act_area_input],
    'Posthumous Combined': [posthumous_combined_input]
})

input_prediction = model.predict(user_input_df)
st.write(input_prediction)


#or i also tried with 
# Handle missing values with imputation
imputer = SimpleImputer(strategy='mean')
data_imputed = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)

y = data['sold_in_USD']
st.write(y)
X = data.drop('sold_in_USD',1, inplace = True)
st.write(data)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestRegressor()
model.fit(X_train, y_train)

# User input
artist_name_input = st.text_input('Artist Name')
birth_year_input = st.number_input('Birth Year', min_value=0, max_value=2023, step=1)
age_input = st.number_input('Age', min_value=0, max_value=120, step=1)
length_input = st.number_input('Length', min_value=0.00, step= 0.001)
width_input = st.number_input('Width', min_value=0.00, step= 0.001)
title_input = st.text_input('Title')
height_input = st.number_input('Height', min_value=0.00, step=0.001)
creation_year_input = st.number_input('Creation Year', min_value=1000, max_value=2023, step=1)
age_at_creation_input = st.number_input('Age of Artist at Creation', min_value=0, max_value=120, step=1)
lower_est_usd_input = st.number_input('Lower Est. USD', min_value=0.00, step=0.01)
upper_est_usd_input = st.number_input('Upper Est. USD', min_value=0.00, step=0.01)
material_category_input = st.selectbox('Material Category', filter_options)
act_area_input = st.selectbox('Act. Area', df['Act. Area'].unique())
posthumous_combined_input = st.selectbox('Posthumous Combined', [0, 1])

# Combine user inputs into a DataFrame for prediction
user_input_df = pd.DataFrame({
    'Artist Name': [artist_name_input],
    'Birth Year': [birth_year_input],
    'Age': [age_input],
    'Length': [length_input],
    'Width': [width_input],
    'Title': [title_input],
    'Height': [height_input],
    'Creation Year': [creation_year_input],
    'Age of Artist at Creation': [age_at_creation_input],
    'Lower Est. USD': [lower_est_usd_input],
    'Upper Est. USD': [upper_est_usd_input],
    'Material Category': [material_category_input],
    'Act. Area': [act_area_input],
    'Posthumous Combined': [posthumous_combined_input]
})


# Impute missing values in user input
user_input_imputed = pd.DataFrame(imputer.transform(user_input_df), columns=user_input_df.columns)

# Make predictions
user_input_reshaped = user_input_imputed.values.reshape(1, -1)
prediction = model.predict(user_input_reshaped)[0]

# Display the prediction
st.write(f'Predicted Sales Amount in USD: {prediction}')


