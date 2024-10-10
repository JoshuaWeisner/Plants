import streamlit as st
import pandas as pd
import numpy as np
import gdown
import os
import plotly.graph_objs as go

st.title('Hydroponics Dashboard')

file_id = '1eARZ0iioA7GDm1fb_b5Vc9gLhVxxxibf'
download_url = f'https://drive.google.com/uc?id={file_id}'

gdown.download(download_url, 'sensor_data.csv', quiet=False)

local = 'sensor_data.csv'

gdown.download(download_url, local, quiet=False)


if os.path.exists(local):
    data = pd.read_csv(local)

    # Display the DataFrame for user reference
    if st.button("Show original data"):
        st.dataframe(data)

    # Select the first four columns excluding the first column
    num_columns = data.shape[1]
    columns_to_plot = data.columns[1:num_columns]  # Get the second to fifth columns
    data.rename(columns={"date_time": "time"}, inplace=True)

    num_plots = len(columns_to_plot)
    for i in range(0, num_plots, 2):
        cols = st.columns(2)  # Create two columns for each iteration

        # Plot the first column in the pair
        with cols[0]:
            if i < num_plots:  # Check if the first plot index is valid
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.iloc[:, 0], y=data[columns_to_plot[i]], mode='lines+markers', name=columns_to_plot[i]))
                fig.update_layout(title=f'Plot of {columns_to_plot[i]} against {data.columns[0]}',
                                  xaxis_title=data.columns[0],
                                  yaxis_title=columns_to_plot[i],
                                  legend_title='Columns')
                st.plotly_chart(fig)

        # Plot the second column in the pair
        with cols[1]:
            if i + 1 < num_plots:  # Check if the second plot index is valid
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.iloc[:, 0], y=data[columns_to_plot[i + 1]], mode='lines+markers', name=columns_to_plot[i + 1]))
                fig.update_layout(title=f'Plot of {columns_to_plot[i + 1]} against {data.columns[0]}',
                                  xaxis_title=data.columns[0],
                                  yaxis_title=columns_to_plot[i + 1],
                                  legend_title='Columns')
                st.plotly_chart(fig)


else:
    st.write("File not found.")

