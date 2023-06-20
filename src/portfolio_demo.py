import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# from streamlit_echarts import st_echarts
from sir import SIR_arr, get_lambda

st.set_page_config(layout='wide')

EN_pop = pd.read_csv('./BEEPmbp-COVID-19-analysis/COVID 19 England/Data_England_AS/population.csv')
EN_pop = EN_pop.T.iloc[1:].rename(columns={0:'England'})


EN_contact_matrix = pd.read_csv('./BEEPmbp-COVID-19-analysis/COVID 19 England/Data_England_AS/age_mixing_matrix.csv', header=None) #, columns=EN_pop.index, index=EN_pop.index)
#EN_contact_matrix = EN_contact_matrix.shift(1)
#EN_contact_matrix.iloc[0] = EN_contact_matrix.columns
#EN_contact_matrix = EN_contact_matrix.astype(float)
EN_contact_matrix.columns = EN_pop.index
EN_contact_matrix = EN_contact_matrix.set_index(EN_pop.index).round(1)


cols = st.columns([0.05, 0.45, 0.45, 0.05])


# fig = go.Figure(
#     go.Bar(
#         x = EN_pop.index,
#         y = EN_pop['England'].values
#     ), 
#     # title_text='England: Population Distribution by Age'
# )

# fig.update_layout(
#     title={
#         'text': "England: Population Distribution by Age",})

# with cols[1]:
#     st.plotly_chart(fig, use_container_width=True)

fig, ax = plt.subplots()
EN_pop.plot.bar(ax=ax, color='w', edgecolor='k')
plt.xticks(rotation=60)
plt.title('England: Population Distribution by Age')
with cols[1]:
    st.pyplot(fig)


fig = plt.figure(figsize=(10, 8))
plt.imshow(EN_contact_matrix.values, cmap='Reds')
plt.xticks(range(len(EN_contact_matrix.columns)), EN_contact_matrix.columns, rotation=-45)
plt.yticks(range(len(EN_contact_matrix.columns)), EN_contact_matrix.columns)#, rotation=-45)
plt.title('Age Mixing Matrix: # of contacts / day')
plt.colorbar()

with cols[2]:
    st.pyplot(fig)


lambda_ = get_lambda(EN_contact_matrix.values, EN_pop.values.T[0])
Gamma = 1/14
Beta_ = 5*Gamma/lambda_
Beta = Beta_*EN_contact_matrix.values

I0 = 1
a = SIR_arr((EN_pop.values.T[0] -I0).tolist(), [I0]*EN_pop.shape[0], [0]*EN_pop.shape[0], Beta.tolist(), Gamma, 0.01, EN_pop.index.tolist())
a.run(200)
fig, ax = plt.subplots()

for k in range(a.n_groups):
    ax.plot(a.time_vector, a.I_timecourse(k), label=a.group_labels[k], color=plt.cm.Reds(10*k))
ax.set_title('I(t)')
# ax.legend()
        
fig.show()
fig.tight_layout()
# with cols[2]:
st.pyplot(fig)

fig, ax = plt.subplots()

for k in range(a.n_groups):
    ax.plot(a.time_vector, np.asarray(a.I_timecourse(k))/EN_pop.iloc[k].England, label=a.group_labels[k], color=plt.cm.Reds(10*k))
ax.set_title('I(t)')
# ax.legend()
        
fig.show()
fig.tight_layout()
# with cols[2]:
st.pyplot(fig)

# options={
#         'title': {
#             'top': 30,
#             'left': 'center',
#             'text': 'England Contact Matrix',
#             # 'textStyle': {'fontFamily': 'monospace'}
#         },

#         'xAxis': {
#         'type': 'category',
#         'data': list(EN_contact_matrix.columns)[::-1],
#         'splitArea': {
#         'show': 'true'
#         }
#         },
#     'yAxis': {
#         'type': 'category',
#         'data': list(EN_contact_matrix.index),
#         'splitArea': {
#         'show': 'true'
#         },
#     },
#     'visualMap': {
#         'show': 'false',
#         # 'padding': 5,
#         'min': 0,
#         'max': 10,
#         'inRange' : {   
#             'color': ['#ffffff', '#EE6363' ] 
#         },
#         'calculable': 'true',
#         'orient': 'horizontal',
#         'left': 'center',
#         'bottom': '0%',
#         # 'controller':{}
#         },
#         'series': [
#         {
#             'name': 'Net Currency Pair Cashflow',
#             'type': 'heatmap',
#             'data': [(a, b, EN_contact_matrix[a].loc[b]) for a in EN_contact_matrix.columns for b in EN_contact_matrix.columns],
#             'label': {
#                 'show': 'true'
#             },
#             'emphasis': {
#                 'itemStyle': {
#                 'shadowBlur': 10,
#                 'shadowColor': 'rgba(0, 0, 0, 0.5)'
#                 }
#             }
#             }
#         ]
#         }

# st_echarts(options=options, height='400px')