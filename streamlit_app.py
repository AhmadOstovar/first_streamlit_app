import streamlit
import pandas as pd
import requests

streamlit.title('My First Streamlit!')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt") 
my_fruit_list = my_fruit_list.set_index('Fruit')

#Lets put a pick list here so they can pick the fruit they want to include
# streamlit.multiselect("pick some fruits:", list(my_fruit_list['Fruit']))
fruits_selected = streamlit.multiselect("pick some fruits:", list(my_fruit_list.index),['Grapes','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected] 

#Display the table on the page
streamlit.dataframe(fruits_to_show)

#New section to display fruityvice response
streamlit.header('Fruityvice Fruit Advice!')

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response)
# streamlit.text(fruityvice_response.json()['name'])
# streamlit.text(fruityvice_response.json())   #just writing the data to the screen

fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)
