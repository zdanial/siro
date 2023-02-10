import streamlit as st
import numpy as np
import plotly.graph_objects as go

import sirO
st.title('Hello')
runtime = 100
dt = 0.01
S0 = st.slider('S', 100, 1000, 100)
S, I, R = sirO.sir(runtime, dt, S0, 1, 0, 
    [1 for i in range(int(runtime//dt)+1)], 
    [1/14 for i in range(int(runtime//dt)+1)],
    [0.005 for i in range(int(runtime//dt)+1)] )

t_vector = np.arange(0, runtime+dt, dt)
fig = go.Figure([
    go.Scatter(x=t_vector, y=S, name='S'),
    go.Scatter(x=t_vector, y=I, name='I'),
    go.Scatter(x=t_vector, y=R, name='R')
    ])
st.plotly_chart(fig)