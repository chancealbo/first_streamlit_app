import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('My Parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avamacado toasties')
   
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.

streamlit.dataframe(fruits_to_show)

# API
streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")


# normalized data 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# displayed data in dataframe
streamlit.dataframe(fruityvice_normalized)

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")


add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'brown')

result = streamlit.button("Add Fruit")
if result:
   my_cur.execute("INSERT INTO fruit_load_list VALUES " +  "    ('{}') ".format(add_my_fruit))
   my_cur.execute("SELECT * FROM fruit_load_list")
   my_data_rows = my_cur.fetchall()
   streamlit.header("The Fruit Load List Contains:")
   streamlit.dataframe(my_data_rows)
