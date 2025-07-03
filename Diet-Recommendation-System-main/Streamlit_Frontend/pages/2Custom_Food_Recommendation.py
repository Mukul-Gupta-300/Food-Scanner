import streamlit as st
from Generate_Recommendations import Generator
from ImageFinder.ImageFinder import get_images_links as find_image
from PIL import Image
import pandas as pd
import base64
from streamlit_echarts import st_echarts


def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
logo_path = "C:/games/coding/nutrition/Diet-Recommendation-System-main/Streamlit_Frontend/logo.jpeg"
encoded_logo = get_image_base64(logo_path)


st.set_page_config(page_title="Custom Food Recommendation",layout="wide")
nutrition_values=['Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent']
if 'generated' not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations=None

# Custom CSS for styling
st.markdown(f"""
<style>
    /* Main container adjustments */
    .reportview-container .main .block-container {{
        padding-top: 0rem;
    }}

    /* Logo styling - ensure aspect ratio */
    .logo-img {{
        max-width: 100px; /* Adjust the maximum width */
        height: auto; /* Maintain aspect ratio */
        margin: 0 auto 20px auto; /* Center the logo and add bottom margin */
        display: block;
    }}

    /* Title and header styling */
    .logo-title {{
        font-size: 48px;
        font-weight: bold;
        text-align: center; /* Center-align title */
        margin-bottom: 10px; /* Reduce bottom margin for better spacing */
    }}

    /* Sidebar content styling (optional) */
    .sidebar .sidebar-content {{
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    /* Sidebar logo (optional) */
    .sidebar-logo {{
        width: 100px;
        margin-bottom: 20px;
    }}

    /* Header and sub-header styling */
    .header {{
        text-align: center;
        font-family: sans-serif;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 10px; /* Reduce margin for better alignment */
    }}

    .sub-header {{
        text-align: center;
        font-family: sans-serif;
        font-size: 24px;
        margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# HTML for displaying logo and titles
st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <img src="data:image/jpeg;base64,{encoded_logo}" class="logo-img">
    </div>
""", unsafe_allow_html=True)




class Recommendation:
    def __init__(self,nutrition_list,nb_recommendations,ingredient_txt):
        self.nutrition_list=nutrition_list
        self.nb_recommendations=nb_recommendations
        self.ingredient_txt=ingredient_txt
        pass
    def generate(self,):
        params={'n_neighbors':self.nb_recommendations,'return_distance':False}
        ingredients=self.ingredient_txt.split(';')
        generator=Generator(self.nutrition_list,ingredients,params)
        recommendations=generator.generate()
        recommendations = recommendations.json()['output']
        if recommendations!=None:              
            for recipe in recommendations:
                recipe['image_link']=find_image(recipe['Name'])
        return recommendations

class Display:
    def __init__(self):
        self.nutrition_values=nutrition_values

    def display_recommendation(self, recommendations):
        st.subheader('Recommended recipes:')
        if recommendations is not None:
            rows = len(recommendations) // 5
            for column, row in zip(st.columns(5), range(5)):
                with column:
                    for recipe in recommendations[rows * row:rows * (row + 1)]:
                        recipe_name = recipe['Name']
                        if st.button(recipe_name):
                            st.session_state['selected_recipe'] = recipe
                            st.session_state['show_expander'] = True

            if st.session_state.get('show_expander', False) and 'selected_recipe' in st.session_state:
                self.show_recipe_expander(st.session_state['selected_recipe'])
        else:
            st.info('Couldn\'t find any recipes with the specified ingredients', icon="🙁")

    def show_recipe_expander(self, recipe):
        with st.expander(f"Recipe: {recipe['Name']}", expanded=True):
            recipe_link = recipe['image_link']
            recipe_img = f'<div><center><img src={recipe_link} alt={recipe["Name"]}></center></div>'
            nutritions_df = pd.DataFrame({value: [recipe[value]] for value in self.nutrition_values})

            st.markdown(recipe_img, unsafe_allow_html=True)
            st.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values (g):</h5>', unsafe_allow_html=True)
            st.dataframe(nutritions_df)
            st.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Ingredients:</h5>', unsafe_allow_html=True)
            for ingredient in recipe['RecipeIngredientParts']:
                st.markdown(f"- {ingredient}")
            st.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Recipe Instructions:</h5>', unsafe_allow_html=True)
            for instruction in recipe['RecipeInstructions']:
                st.markdown(f"- {instruction}")
            st.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Cooking and Preparation Time:</h5>', unsafe_allow_html=True)
            st.markdown(f"""
                - Cook Time       : {recipe['CookTime']}min
                - Preparation Time: {recipe['PrepTime']}min
                - Total Time      : {recipe['TotalTime']}min
            """)
    def display_overview(self,recommendations):
        if recommendations!=None:
            st.subheader('Overview:')
            col1,col2,col3=st.columns(3)
            with col2:
                selected_recipe_name=st.selectbox('Select a recipe',[recipe['Name'] for recipe in recommendations])
            st.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values:</h5>', unsafe_allow_html=True)
            for recipe in recommendations:
                if recipe['Name']==selected_recipe_name:
                    selected_recipe=recipe
            options = {
        "title": {"text": "Nutrition values", "subtext": f"{selected_recipe_name}", "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left",},
        "series": [
            {
                "name": "Nutrition values",
                "type": "pie",
                "radius": "50%",
                "data": [{"value":selected_recipe[nutrition_value],"name":nutrition_value} for nutrition_value in self.nutrition_values],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }
            st_echarts(options=options, height="600px",)

title="<h1 style='text-align: center;'>Custom Food Recommendation</h1>"
st.markdown(title, unsafe_allow_html=True)


display=Display()

import streamlit as st

# Function to synchronize input fields
def sync_input_fields(key, default_value):
    if key not in st.session_state:
        st.session_state[key] = default_value

# Initialize session state values
sync_input_fields('Calories_input', 500)
sync_input_fields('FatContent_input', 50)
sync_input_fields('SaturatedFatContent_input', 0)
sync_input_fields('CholesterolContent_input', 0)
sync_input_fields('SodiumContent_input', 400)
sync_input_fields('CarbohydrateContent_input', 100)
sync_input_fields('FiberContent_input', 10)
sync_input_fields('SugarContent_input', 10)
sync_input_fields('ProteinContent_input', 10)

# Define your form
with st.form("recommendation_form"):
    st.header('Nutritional values:')

    # Input fields for nutritional values
    st.number_input('Calories', min_value=0, max_value=2000, value=st.session_state['Calories_input'], step=10, key='Calories_input')
    st.number_input('Fat Content', min_value=0, max_value=100, value=st.session_state['FatContent_input'], step=1, key='FatContent_input')
    st.number_input('Saturated Fat Content', min_value=0, max_value=13, value=st.session_state['SaturatedFatContent_input'], step=1, key='SaturatedFatContent_input')
    st.number_input('Cholesterol Content', min_value=0, max_value=300, value=st.session_state['CholesterolContent_input'], step=1, key='CholesterolContent_input')
    st.number_input('Sodium Content', min_value=0, max_value=2300, value=st.session_state['SodiumContent_input'], step=100, key='SodiumContent_input')
    st.number_input('Carbohydrate Content', min_value=0, max_value=325, value=st.session_state['CarbohydrateContent_input'], step=1, key='CarbohydrateContent_input')
    st.number_input('Fiber Content', min_value=0, max_value=50, value=st.session_state['FiberContent_input'], step=1, key='FiberContent_input')
    st.number_input('Sugar Content', min_value=0, max_value=40, value=st.session_state['SugarContent_input'], step=1, key='SugarContent_input')
    st.number_input('Protein Content', min_value=0, max_value=40, value=st.session_state['ProteinContent_input'], step=1, key='ProteinContent_input')

    st.header('Recommendation options (OPTIONAL):')
    nb_recommendations = st.slider('Number of recommendations', 5, 20, step=5)
    ingredient_txt = st.text_input('Specify ingredients to include in the recommendations separated by ";" :', placeholder='Ingredient1;Ingredient2;...')
    st.caption('Example: Milk;eggs;butter;chicken...')
    
    # Submit button
    generated = st.form_submit_button("Generate")

if generated:
    with st.spinner('Generating recommendations...'): 
        recommendation = Recommendation(
            [
                st.session_state['Calories_input'],
                st.session_state['FatContent_input'],
                st.session_state['SaturatedFatContent_input'],
                st.session_state['CholesterolContent_input'],
                st.session_state['SodiumContent_input'],
                st.session_state['CarbohydrateContent_input'],
                st.session_state['FiberContent_input'],
                st.session_state['SugarContent_input'],
                st.session_state['ProteinContent_input']
            ],
            nb_recommendations,
            ingredient_txt
        )
        recommendations = recommendation.generate()
        st.session_state.recommendations = recommendations
    st.session_state.generated = True

if st.session_state.get('generated', False):
    with st.container():
        display.display_recommendation(st.session_state.recommendations)
    with st.container():
        display.display_overview(st.session_state.recommendations)

# Footer with logo
st.markdown("""
<style>
    .logo-footer {
        text-align: center;
        margin-top: 30px;
    }
    .logo-footer img {
        width: 100px;
        height: auto;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="logo-footer">
        <img src="data:image/jpeg;base64,{encoded_logo}" alt="Nutridex Logo">
        <p>Powered by Nutridex</p>
    </div>
""", unsafe_allow_html=True)
