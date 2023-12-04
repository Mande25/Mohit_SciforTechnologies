import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

bitcoin_data = pd.read_csv('D:/Scifor mini project/coin_Bitcoin.csv')
litecoin_data = pd.read_csv('D:/Scifor mini project/coin_Litecoin.csv')
ethereum_data = pd.read_csv('D:/Scifor mini project/coin_Ethereum.csv')

# Function to create Line Chart
def plot_line_chart(data, title):
    chart = alt.Chart(data).mark_line().encode(
        x='Date:T',
        y='Close:Q',
        tooltip=['Date:T', 'Close:Q']
    ).properties(title=title)
    st.altair_chart(chart, use_container_width=True)




# Function to create Rolling Average plot
def plot_rolling_average(data, title):
    sampled_data = data.sample(5)  # Sample 5 dates for better readability
    rolling_avg = sampled_data['Close'].rolling(window=30).mean()  # 30-day rolling average

    chart = alt.Chart(sampled_data).mark_line(point=True).encode(
        x='Date:T',
        y=alt.Y('Close:Q', title='Price'),
        color=alt.Color('type:N', scale=alt.Scale(range=['blue', 'red']), title='Type'),
        tooltip=['Date:T', 'Close:Q']
    ).transform_fold(
        ['Close', 'Rolling Average'],
        as_=['type', 'value']
    ).properties(title=title)
    st.altair_chart(chart, use_container_width=True)

# Function to create Volume vs Close Price Scatter plot
def plot_volume_price_scatter(data, title):
    chart = alt.Chart(data).mark_circle().encode(
        x=alt.X('Volume:Q', scale=alt.Scale(type='log'), title='Volume'),
        y=alt.Y('Close:Q', scale=alt.Scale(type='log'), title='Close Price'),
        tooltip=['Volume:Q', 'Close:Q']
    ).properties(title=title)
    st.altair_chart(chart, use_container_width=True)

# Function to create Correlation Heatmap
def plot_correlation_heatmap(data, title):
    corr_matrix = data.corr()

    chart = alt.Chart(pd.melt(corr_matrix.reset_index(), id_vars='index')).mark_rect().encode(
        x='index:O',
        y='variable:O',
        color='value:Q'
    ).properties(title=title)
    st.altair_chart(chart, use_container_width=True)

# Function to create Regression plot
def plot_regression(data, title, x_col, y_col):
    chart = alt.Chart(data).mark_circle().encode(
        x=f'{x_col}:Q',
        y=f'{y_col}:Q',
        tooltip=[f'{x_col}:Q', f'{y_col}:Q']
    ).properties(title=title)
    st.altair_chart(chart, use_container_width=True)


# Function to create Average Closing Price by Year bar plot
def plot_avg_closing_price_by_year(data, title):
    data['Year'] = pd.to_datetime(data['Date']).dt.year
    avg_closing_price_by_year = data.groupby('Year')['Close'].mean().reset_index()

    chart = alt.Chart(avg_closing_price_by_year).mark_bar().encode(
        x='Year:O',
        y='Close:Q',
        tooltip=['Year:O', 'Close:Q']
    ).properties(title=title)
    st.altair_chart(chart, use_container_width=True)

# Function to create Total Volume by Month bar plot
def plot_total_volume_by_month(data, title):
    data['Month'] = pd.to_datetime(data['Date']).dt.month
    total_volume_by_month = data.groupby('Month')['Volume'].sum().reset_index()

    chart = alt.Chart(total_volume_by_month).mark_bar().encode(
        x='Month:O',
        y='Volume:Q',
        tooltip=['Month:O', 'Volume:Q']
    ).properties(title=title)
    st.altair_chart(chart, use_container_width=True)

# Function to create Maximum High Price by Year bar plot
def plot_max_high_price_by_year(data, title):
    # Check if 'Year' column exists, create it otherwise
    if 'Year' not in data.columns:
        data['Year'] = pd.to_datetime(data['Date']).dt.year

    try:
        max_high_price_by_year = data.groupby('Year')['High'].max().reset_index()

        chart = alt.Chart(max_high_price_by_year).mark_bar().encode(
            x='Year:O',
            y='High:Q',
            tooltip=['Year:O', 'High:Q']
        ).properties(title=title)
        st.altair_chart(chart, use_container_width=True)

    except KeyError:
        st.warning("No data available for the selected visualization.")


st.title("Cryptocurrency Interactive Dashboard")

# Sidebar for coin selection
coin_selection = st.sidebar.selectbox("Select Coin", ['Bitcoin', 'Litecoin', 'Ethereum'])

# Display visualizations based on selected coin
selected_data = None
if coin_selection == 'Bitcoin':
    selected_data = bitcoin_data
elif coin_selection == 'Litecoin':
    selected_data = litecoin_data
elif coin_selection == 'Ethereum':
    selected_data = ethereum_data

# Sidebar for visualization selection
selected_function = st.sidebar.selectbox("Select Visualization", [
    'Rolling Average Plot',
    'Volume vs Close Price Scatter Plot',
    'Correlation Heatmap',
    'Line Chart',
    'Regression Plot',
    'Average Closing Price by Year',
    'Total Volume by Month',
    'Maximum High Price by Year',
])

if selected_data is not None:
    st.subheader(selected_function)

    # Add your function calls here based on the selected visualization
    if selected_function == 'Line Chart':
        plot_line_chart(selected_data, f'{coin_selection} - {selected_function}')
    elif selected_function == 'Rolling Average Plot':
        # Call the corresponding function from data_visual.ipynb
        plot_rolling_average(selected_data, f'{coin_selection} - {selected_function}')
    elif selected_function == 'Volume vs Close Price Scatter Plot':
        # Call the corresponding function from data_visual.ipynb
        plot_volume_price_scatter(selected_data, f'{coin_selection} - {selected_function}')
    elif selected_function == 'Correlation Heatmap':
        # Call the corresponding function from data_visual.ipynb
        plot_correlation_heatmap(selected_data, f'{coin_selection} - {selected_function}')
    elif selected_function == 'Regression Plot':
        # Call the corresponding function from data_visual.ipynb
        plot_regression(selected_data, f'{coin_selection} - {selected_function}', 'Open', 'Close')
    elif selected_function == 'Average Closing Price by Year':
        plot_avg_closing_price_by_year(selected_data, f'{coin_selection} - {selected_function}')
    elif selected_function == 'Total Volume by Month':
        plot_total_volume_by_month(selected_data, f'{coin_selection} - {selected_function}')
    elif selected_function == 'Maximum High Price by Year':
        plot_max_high_price_by_year(selected_data, f'{coin_selection} - {selected_function}')
