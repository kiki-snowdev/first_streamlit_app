import streamlit
import pandas
import requests
import snowflake.connector;
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled, Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)

#section to show fruityvice response
streamlit.header("Fruityvice Fruit Advice!")

#function to get fruityvice data
def get_fruityvice_data(this_fruit_choice):
  #import requests
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +  this_fruit_choice) #sends a request and gets a json response
  # streamlit.text(fruityvice_response.json()) -- writes the json response to the screen
  # normalises the json response 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
   
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information')
  else:
    result_fruitvice_data = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(result_fruitvice_data)
     
except URLError as e:
  streamlit.error()


#stop here to troubleshoot

#import snowflake.connector;

streamlit.header("View Our Fruits List - Add your Favourites!")
#building a snowflake function
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

  #adding a button to get list
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)
  

 
def insert_to_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return "Thank you for adding " +new_fruit

add_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_to_snowflake(add_fruit)
  my_cnx.close()
  streamlit.write(back_from_function)
streamlit.stop()


