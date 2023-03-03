import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  # streamlit.write('The user entered', fruit_choice)
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
   else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # streamlit.text(fruityvice_response)
    # streamlit.text(fruityvice_response.json()['name'])
    # streamlit.text(fruityvice_response.json())   #just writing the data to the screen
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
    
except URLError as e:
  streamlit.error()
# ------------------------------------------------------
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)
# ------------------------------------------------------
#do not run anything past here while we troubleshoot
streamlit.stop()
# ------------------------------------------------------
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)
# streamlit.text("The fruit load list contains:")
# streamlit.text(my_data_row)
# ------------------------------------------------------
# streamlit.header('What fruit would you like to add?')
fruit_choice = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding', fruit_choice)
#----------------------------------------------------------------
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values ('from streamlit')")
