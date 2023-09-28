import streamlit as st
import pandas as pd
import numpy as np
import openai,sys
import json


openai.api_key = "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"

st.title('BIOMASS RECOMMENDER')

biomass_data = pd.read_excel("Biomass_Dataset.xlsx")
option = st.selectbox(
    'What state are you looking into?',
    biomass_data['LGA'].values)

food_crops = [i.strip() for i in biomass_data[biomass_data['LGA']==option]['Food crops'].values[0].split(',')]
cook_heat = [i.strip() for i in biomass_data[biomass_data['LGA']==option]['Cooking and Heating Materials'].values[0].split(',')]
bio_char =[i.strip() for i in biomass_data[biomass_data['LGA']==option]['Biochar Materials'].values[0].split(',')]
bio_energy = [i.strip() for i in biomass_data[biomass_data['LGA']==option]['Bioenergy Materials'].values[0].split(',')]
editor_df = pd.DataFrame({'Food Crop':food_crops,'mark':[False for i in range(len(food_crops))]})
raw_materials = st.selectbox('What Raw Materials do you wish to check for its biomass material ',editor_df)

#st.write(raw_materials,bio_char,bio_enegry,cook_heat)

def get_response(raw_materials,bio_energy,bio_char,cook_heat):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": f"""
                    You will be given a food crop : {raw_materials}. 
                    return just a JSON format with the following key value pairs in back ticks.
                    
                    `Selected_Raw_Material`- `The particular food crop you are working on`
                    `Bio_energy`-`Based on {bio_energy} list, kindly return all the bio- energy material in the list that can be gotten from the selected raw materials and if any of the name in the list begins with the selected raw material also return it if none can be gotten, return None`
                    `Bio_energy_Description`- A very Brief Description of each of the `bio-energy materials` can be used for and some important information about it, less than 200 words`                      `
                    `Biochar`-`Based on {bio_char} lisr, kindly return all the `bio-char material` in the list that can be gotten from the selected raw materials and if any of the name in the list begins with the selected raw material also return it.if none can be gotten, return None`
                    `Biochar_Description`- A very Brief Description of each of the bio char materials can be used for and some important information about it, less than 200 words`
                    `Cooking and Heating Materials`-`Based on {cook_heat} list, kindly return all the  `Cooking and Heating material` in the list that can be gotten from the selected raw materials, and if any of the name in the list begins with the selected raw material also return itif none can be gotten, return None`
                    `Cooking and Heating Materials_Description`- A very Brief Description of each of the Cooking and Heating Material can be used for and some important information about it, less than 200 words`
                        
                    
                        """
        }
      ],
      temperature=0
    )
    return response['choices'][0]['message']['content']

if len(raw_materials)!=0:
    #st.json(get_response(raw_materials,bio_energy,bio_char,cook_heat))
    json_string = get_response(raw_materials,bio_energy,bio_char,cook_heat)
    data_dict = json.loads(json_string)
    
    
    st.header(data_dict['Selected_Raw_Material'].capitalize())
    st.divider()
    if data_dict['Bio_energy'] is not None:
        st.subheader('Bio_Energy')
        for j,k in enumerate(data_dict['Bio_energy']):
            st.markdown(f'- {k}')
        st.subheader(f'Description')
        st.markdown(f"\n\t{data_dict['Bio_energy_Description']}")
        st.divider()
    st.divider()
    if data_dict['Biochar'] is not None:
        st.subheader('Biochar')
        for j,k in enumerate(data_dict['Biochar']):
            st.markdown(f'- {k}')
        st.subheader(f'Description')
        st.markdown(f"\n\t{data_dict['Biochar_Description']}")
        st.divider()
    st.divider()
    if data_dict['Cooking and Heating Materials'] is not None:
        st.subheader('Cooking and Heating Materials')
        for j,k in enumerate(data_dict['Cooking and Heating Materials']):
            st.markdown(f'- {k}')
        st.subheader(f'Description')
        st.markdown(f"\n\t{data_dict['Cooking and Heating Materials_Description']}")
        st.divider()