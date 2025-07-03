import streamlit as st
import pandas as pd
from Generate_Recommendations import Generator
from PIL import Image
import base64
from random import uniform as rnd
from ImageFinder.ImageFinder import get_images_links as find_image
from streamlit_echarts import st_echarts
from streamlit_modal import Modal as md

def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_path = "C:/games/coding/nutrition/Diet-Recommendation-System-main/Streamlit_Frontend/logo.jpeg"
encoded_logo = get_image_base64(logo_path)

st.set_page_config(page_title="Diet Recommendation",layout="wide")


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


nutritions_values=['Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent']
# Streamlit states initialization
if 'person' not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations=None
    st.session_state.person=None
    st.session_state.weight_loss_option=None
class Person:

    def __init__(self,age,height,weight,gender,activity,meals_calories_perc,weight_loss):
        self.age=age
        self.height=height
        self.weight=weight
        self.gender=gender
        self.activity=activity
        self.meals_calories_perc=meals_calories_perc
        self.weight_loss=weight_loss
    def calculate_bmi(self,):
        bmi=round(self.weight/((self.height/100)**2),2)
        return bmi

    def display_result(self,):
        bmi=self.calculate_bmi()
        bmi_string=f'{bmi} kg/m²'
        if bmi<18.5:
            category='Underweight'
            color='Red'
        elif 18.5<=bmi<25:
            category='Normal'
            color='Green'
        elif 25<=bmi<30:
            category='Overweight'
            color='Yellow'
        else:
            category='Obesity'    
            color='Red'
        return bmi_string,category,color

    def calculate_bmr(self):
        if self.gender=='Male':
            bmr=10*self.weight+6.25*self.height-5*self.age+5
        else:
            bmr=10*self.weight+6.25*self.height-5*self.age-161
        return bmr

    def calories_calculator(self):
        activites=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
        weights=[1.2,1.375,1.55,1.725,1.9]
        weight = weights[activites.index(self.activity)]
        maintain_calories = self.calculate_bmr()*weight
        return maintain_calories

    def generate_recommendations(self,):
        total_calories=self.weight_loss*self.calories_calculator()
        recommendations=[]
        for meal in self.meals_calories_perc:
            meal_calories=self.meals_calories_perc[meal]*total_calories
            if meal=='breakfast':        
                recommended_nutrition = [meal_calories,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
            elif meal=='lunch':
                recommended_nutrition = [meal_calories,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)]
            elif meal=='dinner':
                recommended_nutrition = [meal_calories,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)] 
            else:
                recommended_nutrition = [meal_calories,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
            generator=Generator(recommended_nutrition)
            recommended_recipes=generator.generate().json()['output']
            recommendations.append(recommended_recipes)
        for recommendation in recommendations:
            for recipe in recommendation:
                recipe['image_link']=find_image(recipe['Name']) 
        return recommendations


class Display:
    def __init__(self):
        self.plans=["Maintain weight","Mild weight loss","Weight loss","Extreme weight loss"]
        self.weights=[1,0.9,0.8,0.6]
        self.losses=['-0 kg/week','-0.25 kg/week','-0.5 kg/week','-1 kg/week']
        pass

    def display_bmi(self,person):
        st.header('BMI CALCULATOR')
        bmi_string,category,color = person.display_result()
        st.metric(label="Body Mass Index (BMI)", value=bmi_string)
        new_title = f'<p style="font-family:sans-serif; color:{color}; font-size: 25px;">{category}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.markdown(
            """
            Healthy BMI range: 18.5 kg/m² - 25 kg/m².
            """)   

    def display_calories(self,person):
        st.header('CALORIES CALCULATOR')        
        maintain_calories=person.calories_calculator()
        st.write('The results show a number of daily calorie estimates that can be used as a guideline for how many calories to consume each day to maintain, lose, or gain weight at a chosen rate.')
        for plan,weight,loss,col in zip(self.plans,self.weights,self.losses,st.columns(4)):
            with col:
                st.metric(label=plan,value=f'{round(maintain_calories*weight)} Calories/day',delta=loss,delta_color="inverse")

    def display_recommendation(self, person, recommendations):
        # Initialize session state variables at the beginning
        if 'show_expander' not in st.session_state:
            st.session_state['show_expander'] = False
        if 'selected_recipe' not in st.session_state:
            st.session_state['selected_recipe'] = None

        st.header('DIET RECOMMENDATOR')

        with st.spinner('Generating recommendations...'):
            meals = person.meals_calories_perc
            st.subheader('Recommended recipes:')
            
            # Create columns for each meal and display the recommended recipes
            for meal_name, column, recommendation in zip(meals, st.columns(len(meals)), recommendations):
                with column:
                    st.markdown(f'##### {meal_name.upper()}')
                    
                    # Loop through each recipe and add a button for viewing details
                    for idx, recipe in enumerate(recommendation):
                        recipe_name = recipe['Name']
                        button_key = f"view_button_{meal_name}_{recipe_name}_{idx}"

                        if st.button(f"View {recipe_name}", key=button_key):
                            # Store selected recipe and trigger expander display
                            st.session_state['selected_recipe'] = recipe
                            st.session_state['show_expander'] = True

        # Check if a recipe has been selected and show the expander with details
        if st.session_state.get('show_expander', False) and 'selected_recipe' in st.session_state:
            self.show_recipe_expander(st.session_state['selected_recipe'])


    def show_recipe_expander(self, recipe):
        # Display detailed recipe information using an expander
        with st.expander(f"Recipe: {recipe['Name']}"):
            recipe_link = recipe.get('image_link', '')

            # Add custom CSS for centering the image
            if recipe_link:
                st.markdown(
                    """
                    <style>
                    .centered-image img {
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                    }
                    </style>
                    """, unsafe_allow_html=True
                )

                # Display the image if available
                st.markdown(f"<div class='centered-image'><img src='{recipe_link}' width='400'/></div>", unsafe_allow_html=True)

            # Display nutritional values
            st.subheader("Nutritional Values (g):")
            nutritions_values = ["Calories", "ProteinContent", "FatContent", "CarbohydrateContent"]
            nutritions_df = pd.DataFrame({value: [recipe.get(value, 'N/A')] for value in nutritions_values})
            st.dataframe(nutritions_df)

            # Display ingredients
            st.subheader("Ingredients:")
            for ingredient in recipe.get('RecipeIngredientParts', []):
                st.markdown(f"- {ingredient}")

            # Display recipe instructions
            st.subheader("Recipe Instructions:")
            for instruction in recipe.get('RecipeInstructions', []):
                st.markdown(f"- {instruction}")

            # Display cooking and preparation times
            st.subheader("Cooking and Preparation Time:")
            st.markdown(f"""
                - Cook Time: {recipe.get('CookTime', 'N/A')} min
                - Preparation Time: {recipe.get('PrepTime', 'N/A')} min
                - Total Time: {recipe.get('TotalTime', 'N/A')} min
            """)

    # Ensure to initialize session state variables in Streamlit app startup
    if 'show_expander' not in st.session_state:
        st.session_state['show_expander'] = False
    if 'selected_recipe' not in st.session_state:
        st.session_state['selected_recipe'] = None

    def display_meal_choices(self,person,recommendations):    
        st.subheader('Choose your meal composition:')
        # Display meal compositions choices
        if len(recommendations)==3:
            breakfast_column,lunch_column,dinner_column=st.columns(3)
            with breakfast_column:
                breakfast_choice=st.selectbox(f'Choose your breakfast:',[recipe['Name'] for recipe in recommendations[0]])
            with lunch_column:
                luch_choice=st.selectbox(f'Choose your lunch:',[recipe['Name'] for recipe in recommendations[1]])
            with dinner_column:
                dinner_choice=st.selectbox(f'Choose your dinner:',[recipe['Name'] for recipe in recommendations[2]])  
            choices=[breakfast_choice,luch_choice,dinner_choice]     
        elif len(recommendations)==4:
            breakfast_column,morning_snack,lunch_column,dinner_column=st.columns(4)
            with breakfast_column:
                breakfast_choice=st.selectbox(f'Choose your breakfast:',[recipe['Name'] for recipe in recommendations[0]])
            with morning_snack:
                morning_snack=st.selectbox(f'Choose your morning_snack:',[recipe['Name'] for recipe in recommendations[1]])
            with lunch_column:
                lunch_choice=st.selectbox(f'Choose your lunch:',[recipe['Name'] for recipe in recommendations[2]])
            with dinner_column:
                dinner_choice=st.selectbox(f'Choose your dinner:',[recipe['Name'] for recipe in recommendations[3]])
            choices=[breakfast_choice,morning_snack,lunch_choice,dinner_choice]                
        else:
            breakfast_column,morning_snack,lunch_column,afternoon_snack,dinner_column=st.columns(5)
            with breakfast_column:
                breakfast_choice=st.selectbox(f'Choose your breakfast:',[recipe['Name'] for recipe in recommendations[0]])
            with morning_snack:
                morning_snack=st.selectbox(f'Choose your morning_snack:',[recipe['Name'] for recipe in recommendations[1]])
            with lunch_column:
                lunch_choice=st.selectbox(f'Choose your lunch:',[recipe['Name'] for recipe in recommendations[2]])
            with afternoon_snack:
                afternoon_snack=st.selectbox(f'Choose your afternoon:',[recipe['Name'] for recipe in recommendations[3]])
            with dinner_column:
                dinner_choice=st.selectbox(f'Choose your  dinner:',[recipe['Name'] for recipe in recommendations[4]])
            choices=[breakfast_choice,morning_snack,lunch_choice,afternoon_snack,dinner_choice] 
        
        # Calculating the sum of nutritional values of the choosen recipes
        total_nutrition_values={nutrition_value:0 for nutrition_value in nutritions_values}
        for choice,meals_ in zip(choices,recommendations):
            for meal in meals_:
                if meal['Name']==choice:
                    for nutrition_value in nutritions_values:
                        total_nutrition_values[nutrition_value]+=meal[nutrition_value]
  
        total_calories_chose=total_nutrition_values['Calories']
        loss_calories_chose=round(person.calories_calculator()*person.weight_loss)

        # Display corresponding graphs
        st.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Total Calories in Recipes vs {st.session_state.weight_loss_option} Calories:</h5>', unsafe_allow_html=True)
        total_calories_graph_options = {
    "xAxis": {
        "type": "category",
        "data": ['Total Calories you chose', f"{st.session_state.weight_loss_option} Calories"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "data": [
                {"value":total_calories_chose, "itemStyle": {"color":["#33FF8D","#FF3333"][total_calories_chose>loss_calories_chose]}},
                {"value": loss_calories_chose, "itemStyle": {"color": "#3339FF"}},
            ],
            "type": "bar",
        }
    ],
}
        st_echarts(options=total_calories_graph_options,height="400px",)
        st.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values:</h5>', unsafe_allow_html=True)
        nutritions_graph_options = {
    "tooltip": {"trigger": "item"},
    "legend": {"top": "5%", "left": "center"},
    "series": [
        {
            "name": "Nutritional Values",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": "#fff",
                "borderWidth": 2,
            },
            "label": {"show": False, "position": "center"},
            "emphasis": {
                "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
            },
            "labelLine": {"show": False},
            "data": [{"value":round(total_nutrition_values[total_nutrition_value]),"name":total_nutrition_value} for total_nutrition_value in total_nutrition_values],
        }
    ],
}       
        st_echarts(options=nutritions_graph_options, height="500px",)
        

display=Display()
subtitle="<h2 style='text-align: center;'>Automatic Diet Recommendation</h2>"
st.markdown(subtitle, unsafe_allow_html=True)
with st.form("recommendation_form"):
    st.write("Modify the values and click the Generate button to use")
    age = st.number_input('Age',min_value=2, max_value=120, step=1)
    height = st.number_input('Height(cm)',min_value=50, max_value=300, step=1)
    weight = st.number_input('Weight(kg)',min_value=10, max_value=300, step=1)
    gender = st.radio('Gender',('Male','Female'))
    activity = st.select_slider('Activity',options=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 
    'Extra active (very active & physical job)'])
    option = st.selectbox('Choose your weight loss plan:',display.plans)
    st.session_state.weight_loss_option=option
    weight_loss=display.weights[display.plans.index(option)]
    number_of_meals=st.slider('Meals per day',min_value=3,max_value=5,step=1,value=3)
    if number_of_meals==3:
        meals_calories_perc={'breakfast':0.35,'lunch':0.40,'dinner':0.25}
    elif number_of_meals==4:
        meals_calories_perc={'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'dinner':0.25}
    else:
        meals_calories_perc={'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'afternoon snack':0.05,'dinner':0.20}
    generated = st.form_submit_button("Generate")
if generated:
    st.session_state.generated=True
    person = Person(age,height,weight,gender,activity,meals_calories_perc,weight_loss)
    with st.container():
        display.display_bmi(person)
    with st.container():
        display.display_calories(person)
    with st.spinner('Generating recommendations...'):     
        recommendations=person.generate_recommendations()
        st.session_state.recommendations=recommendations
        st.session_state.person=person

if st.session_state.generated:
    with st.container():
        display.display_recommendation(st.session_state.person,st.session_state.recommendations)
        st.success('Thanks for choosing Nutridex!')
    with st.container():
        display.display_meal_choices(st.session_state.person,st.session_state.recommendations)

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


# st.sidebar.markdown('<div class="sidebar-item">💪 Diet Recommendation</div>', unsafe_allow_html=True)
# st.sidebar.markdown('<div class="sidebar-item">🔍 Custom Food Recommendation</div>', unsafe_allow_html=True)

# # Add this to your custom CSS
# st.markdown("""
# <style>
#     .sidebar-item {
#         padding: 10px;
#         background-color: #ffffcc;  # Lighter yellow for items
#         margin-bottom: 10px;
#         border-radius: 5px;
#     }
# </style>
# """, unsafe_allow_html=True)