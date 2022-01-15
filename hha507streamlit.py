# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 18:35:54 2022

@author: fabdu
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as pgo
import matplotlib.pyplot as plt
import time


##IMPORT CSV

@st.cache
def load_hospitals():
    hospital_info = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return hospital_info

@st.cache
def load_outpatients():
     outpatient2015 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
     return outpatient2015
 
@st.cache
def load_inpatient():
     inpatient2015 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
     return inpatient2015
 
st.title('HHA 507- Streamlit')
st.write('Fahad Abdu :sunglasses:')


#Load the data
hospital_info = load_hospitals()
inpatient2015 = load_inpatient()
outpatient2015 = load_outpatients()

#Dataframes
st.header('Hospital Data Preview')
st.dataframe(hospital_info)

st.header('Inpatient Data Preview')
st.dataframe(inpatient2015)

st.header('Outpatient Data Preview')
st.dataframe(outpatient2015)

hospital_info['provider_id'] = hospital_info['provider_id'].astype(str)
outpatient2015['provider_id'] = outpatient2015['provider_id'].astype(str)
inpatient2015['provider_id'] = inpatient2015['provider_id'].astype(str)


st.header('Hospital/Inpatient Merged Data')
df_merge_inpt = inpatient2015.merge(hospital_info, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
df_merge_inpt_preview = df_merge_inpt.sample(50)
st.dataframe(df_merge_inpt_preview)

st.header('Hospital/Outpatient Merged Data')
df_merge_outpt = outpatient2015.merge(hospital_info, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
st.dataframe(df_merge_outpt)

st.subheader('Stony Brook Data Hospital/Outpatient')
sb_merge_outpt = df_merge_outpt[df_merge_outpt['provider_name'] == 'University Hospital ( Stony Brook )']
st.dataframe(sb_merge_outpt)

st.subheader('Stony Brook Data Hospital/Inpatient')
sb_merge_inpt = df_merge_inpt[df_merge_inpt['provider_name'] == 'UNIVERSITY HOSPITAL ( STONY BROOK )']
sb_merge_inpt_preview = sb_merge_inpt.sample(10)
st.dataframe(sb_merge_inpt_preview)


st.subheader('Non Stony Brook Data Hospital/Outpatient')
nonsb_merge_outpt = df_merge_outpt[df_merge_outpt['provider_name'] != 'University Hospital ( Stony Brook )']
st.dataframe(nonsb_merge_outpt)

st.subheader('Non Stony Brook Data Hospital/Inpatient')
nonsb_merge_inpt = df_merge_inpt[df_merge_inpt['provider_name'] != 'University Hospital ( Stony Brook )']
nonsb_merge_inpt_preview = nonsb_merge_inpt.sample(10)
st.dataframe(nonsb_merge_inpt_preview)

# Question 1
st.subheader('Question:1')
st.write('How does SB compare to the rest of NY?')
st.markdown('Level IV Endoscopy Upper Airway is the highest treatement cost at Stony Brook at $2307.21. In comparison to other facilities, it is lower. In facilities outside of Stony Brook, 0074 is also the most expensive with the average total payment at $2783.80.')

st.subheader('Stony Brook Outpatient APCs')
SB_Outpatient_APCs_pivot = sb_merge_outpt.pivot_table(index=['provider_id','apc'],values=['average_total_payments'])
SB_Outpatient_APCs_pivot_desc = SB_Outpatient_APCs_pivot.sort_values(['average_total_payments'], ascending=False)
st.dataframe(SB_Outpatient_APCs_pivot_desc)

st.subheader('Non-Stony Brook Outpatient APCs')
NonSB_Outpatient_APCs_pivot = nonsb_merge_outpt.pivot_table(index=['provider_id','apc'],values=['average_total_payments'])
NonSB_Outpatient_APCs_pivot_desc = NonSB_Outpatient_APCs_pivot.sort_values(['average_total_payments'], ascending=False)
st.dataframe(NonSB_Outpatient_APCs_pivot_desc)

# Question 2
st.subheader('Question 2')
st.write('Question 2: How does SB compare to the most expensive inpatient DRGs')
st.markdown('Stony Brook and other inpatient facilities share the same high cost for most expesnive DRGs. 003- 003 - ECMO OR TRACH W MV >96 HRS OR PDX EXC FACE, MOUTH & NECK W MAJ O.R. costs roughly the same amount at $2,166,36.88.')

st.subheader('Stony Brook Inpatient DRGs')
SB_Inpatient_DRGs_pivot = sb_merge_inpt.pivot_table(index=['provider_id','drg_definition'],values=['average_total_payments'])
SB_Inpatient_DRGs_pivot_desc = SB_Inpatient_DRGs_pivot.sort_values(['average_total_payments'], ascending=False)
st.dataframe(SB_Inpatient_DRGs_pivot_desc)

st.subheader('Non-Stony Brook Inpatient DRGs')
NonSB_Inpatient_DRGs_pivot = nonsb_merge_inpt.pivot_table(index=['provider_id','drg_definition'],values=['average_total_payments'])
NonSB_Inpatient_DRGs_pivot_desc = NonSB_Inpatient_DRGs_pivot.sort_values(['average_total_payments'], ascending=False)
st.dataframe(NonSB_Inpatient_DRGs_pivot_desc)

st.subheader('All NY data except Stony Brook (Outpatient)')
NY_nonsb_merge_outpt = nonsb_merge_outpt[nonsb_merge_outpt['provider_state'] == 'NY']
NY_nonsb_merge_outpt_preview = NY_nonsb_merge_outpt.sample(20)
st.dataframe(NY_nonsb_merge_outpt_preview)

st.subheader('All NY data except Stony Brook (Inpatient)')
NY_nonsb_merge_inpt = nonsb_merge_inpt[nonsb_merge_inpt['provider_state'] == 'NY']
NY_nonsb_merge_inpt_preview = NY_nonsb_merge_inpt.sample(20)
st.dataframe(NY_nonsb_merge_inpt_preview)

#Question 3
st.subheader('Question 3')
st.write('Question 3: How does SB compare to the most expensive outpatient DRGs?')
st.markdown('Stony Brook comapred to other NY outpatient facilities share the same most expensive average total payments for 003 at a cost of $2,166,36.')


