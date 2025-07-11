# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
# Write directly to the app
st.title(f" :cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write(
  """ Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The Name on your Smoothie will be : ", name_on_order)
cnx = st.connection('snowflake')
session = cnx.session()
# session = get_active_session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),(col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop
pd_df= my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# convert the snowpark dataframe to a pandas dataframe


ingredients_list = st.multiselect(
                'Choosen up to 5 ingredients: ',
                my_dataframe,
                max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME']== each_fruit,'SEARCH_ON'].iloc(0)
        # st.write('The search value for ', each_fruit,'search_on','.')

        st.subheader(each_fruit + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + each_fruit )
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    #st.write(my_insert_stmt)
    #st.stop()
    # st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")


