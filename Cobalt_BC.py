# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 06:36:46 2022

@author: MC
"""

import geopandas as gpd
import pandas as pd
import streamlit as st


Intro = st.container()
Exploration_1 = st.container()
Exploration_2 = st.container()
Analysis = st.container()
Outro = st.container

with Intro:
    st.title('Cobalt in BC')
    st.markdown('Thanks for checking out my project! My name is Mark and I am a promising Geoscientist with a passion for Data Science')
    st.markdown('In this project I combine my passion for Data with my background in Mining to isolate possible Cobalt deposits')
    st.markdown('The data I am using for this project is "opendata" provided by various government entities both Canadian and American.')
    st.markdown('I take no credit in the procurement and organization of the downloaded government data')
    
with Exploration_1:
    st.title('Identifying Cobalt')
    st.markdown('My goal with this project is to use **geopandas** to highlight possible areas which Cobalt will be found:')
    st.markdown('Due to the limitations of the datasets, there is not exact data on whether an entry contains the element cobalt or not.')
    st.markdown('So we can iterate through our data and search for key minerals obtained from US open data')
    st.markdown('This analysis originally started with both Ontario and BC datasets however the Ontario Dataset did not have enough details to be sufficient for this project.')
    st.markdown('**Important to note**, that while building this project I realized that the data was not detailed enough to be sufficient for our analysis. However the scientific method and code can be updated with better data in the future to bring it to its full potential')
    st.markdown('Lets get started!')
    
with Exploration_2:
    st.title('Exploring our Data')
    st.markdown('First lets import our data through both **Geopandas** and **Pandas** Data Frames')

    with st.echo():
        #Data for British Columbia, provided through government opendata
        BC_Data = gpd.read_file('Data/BC/BC_bedrock_ll83.shp')
        #Data for Critical elements info through government open source data
        Cobalt_Deposits = pd.read_excel('Data/Critical_Elements.xlsx', sheet_name = 'Cobalt', header= 3)
    
    st.markdown('Now we can take a closer look at each Data Frame')
    
    col1,col2 = st.columns(2)
    
    
        
    BC_head = BC_Data.head().drop(columns = 'geometry')
    with col1:
        st.text('British Columbia')
        st.dataframe(BC_head)
        
    with col2:
        st.text('Cobalt Deposits')
        st.dataframe(Cobalt_Deposits)
        
    st.markdown('Now that we have the Data Frames set up we can clean them up for ease of use.')


BC_columns_to_drop = ['strat_name','gp_suite','fm_lithodm','mem_phase','rk_char','basin','basin_age']

BC_Data_cleaning = BC_Data.drop(columns = BC_columns_to_drop)


BC_Data_cleaning['Province']= 'BC'


BC_cleaning_head = BC_Data_cleaning.head()

BC_test = BC_Data_cleaning[['gid','unit_desc','geometry','rock_type']]

BC_clean = BC_test.dropna()

BC_clean = BC_clean.rename(columns={'gid':'geology_id'})
 
with Exploration_2:
    
    st.markdown('Here are the steps I took to clean our data:')
    st.markdown('1. Search for **null** values in the dataset and remove columns with more than **20%** null values')
    st.markdown('2. Now we **remove** the columns that we will not need for our analysis our Data Frames')
    st.markdown('3. Next we rename some columns to make it easier to work with')
    st.markdown('4.Great now we have our clean Data Frame with the shape: 33407,4')
    
    
    st.header('We can now dive deeper into the **Cobalt Deposits** Data Frame')
    st.markdown('The important information in this Data Frame is the **Minerology** Column')
    st.markdown('We will create a list of these indicator **minerals** to aid our analysis')
    
    
    with st.echo():
        #Create an empty list to store values in
        Mineral_list = []
        
        #We iterate over the values in the Mineralogy column of the Data Frame
        for value in Cobalt_Deposits['Mineralogy']:
            value = value.split()
            #We now iterate over the seperate strings in each value
            for string in value:
                string = string.replace(',','')
                if string != 'and':
                    #After removing commas and the word 'and' we append the strings to the list
                    Mineral_list.append(string)
                    
    
    
    st.markdown('Now we iterate through the Dataframe to see if any of these indicator minerals appear in the **unit_desc** of BC Data Frame')
    
    with st.echo():
        #This creates a new column in the dataframe that gives a current value of 1 to all entries
        BC_clean['Cobalt_positive'] = 1
        
        #Begin a count to keep track of index numbers for the dictionary we will create   
        count = -1
        
        #In the following code we convert the values in the unit_desc column into a dict with its index as the key and description as its value
        for value in BC_clean['unit_desc']:
            
            value = value.replace(',','').replace('.','').replace('(','').replace(')','')
            
            count += 1
            
            new_value = {count:value}
            
            #Save the new dicts to the Data Frame
            BC_clean.at[count,'unit_desc'] = new_value
        
        check = 0
        
        #There were two values that did not convert to a dictionary these two entries were removed in the following code
        BC_clean.drop(32500, inplace =True)
        
        BC_clean.drop(33408, inplace =True)
        
        
        #An assertion test to check that every entry was converted to a dict
        for value in BC_clean['unit_desc']:
            
            if not isinstance(value, dict):
                
                assert TypeError('A value in this column is not of type dict') 
        
        counter = 0
        
        #Now we can interate over our column and check how many times our key minerals are found in the descriptions
        for value in BC_clean['unit_desc']:            
            
            (k,v), = value.items()
            
            mineral_count =0
            
            for word in Mineral_list:          
                
                if word in v:
                    
                    mineral_count += 1
                    
            if mineral_count == 0:
                
                #If no minerals were found in an entry we change the column 'Cobalt_positive' to a value of 0
                BC_clean.at[k,'Cobalt_positive'] = 0
                    
            mineral_count = 0
                    
                    
    Contains_Cobalt_Minerals = BC_clean[BC_clean['Cobalt_positive']==1]
    
    for value in Contains_Cobalt_Minerals['unit_desc']:            
        
        (k,v), = value.items()
        
        Contains_Cobalt_Minerals.at[k,'unit_desc'] = v
    
    Contains_Cobalt_Minerals = Contains_Cobalt_Minerals.drop(columns = ['geometry'])


with Analysis:
    st.header('Lets take a look at our final Data Frame')
    st.dataframe(Contains_Cobalt_Minerals)    
    st.markdown('In the end out of the 30000 plus entries in our Data Frame only 31 contained any minerals that were identified from the Cobalt Deposits Data')
    st.markdown('This is not too surprising however for the minerals that were listed are not common minerals. The only common one mentioned was pyrite which at large regional scales would be overlooked in a rock description')
    st.markdown('This project was about the process however and the code did the job I wrote it for.')
    st.header('Conclusion')
    st.markdown('Even though no concrete evidence of Cobalt was found, this is how the process should be. Cobalt is a rare mineral with unique compositions within rocks, and I hope to find data to enhance this project in the future.')
    st.markdown('Thanks for viewing my project - Mark Vaz')
    
  
    

              
            
            
            
            

                    
                    
                    
                    
                
        
                
        
            

       
                    
                    
                    
                    
                    
                    
            
        
                              
                    
                    
                    
                
        
        
    
                
        
        




