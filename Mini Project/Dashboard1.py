import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Hide Streamlit menu
st.set_page_config(
    page_title="Cryptocurrency Interactive Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Remove Streamlit footer
st.markdown(
    """
    <style>
        .viewerBadge_container__1QSob {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


bitcoin_data = pd.read_csv('D:/Scifor mini project/coin_Bitcoin.csv')
litecoin_data = pd.read_csv('D:/Scifor mini project/coin_Litecoin.csv')
ethereum_data = pd.read_csv('D:/Scifor mini project/coin_Ethereum.csv')

def plot_line_chart(data, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    n = max(1, len(data) // 5)  # Display every Nth date
    ax.plot(data['Date'], data['Close'], label='Close Price', marker='o')
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price')
    ax.set_xticks(data['Date'][::n])
    ax.legend()
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
    st.pyplot(fig)

# Function to create candlestick plot
def plot_candlestick(data, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    n = max(1, len(data) // 5)  # Display every Nth date
    sns.lineplot(x='Date', y='Open', data=data, label='Open', marker='o')
    sns.lineplot(x='Date', y='Close', data=data, label='Close', marker='o')
    ax.fill_between(data['Date'], data['Open'], data['Close'], where=data['Open'] > data['Close'], facecolor='red', interpolate=True, alpha=0.3)
    ax.fill_between(data['Date'], data['Open'], data['Close'], where=data['Open'] <= data['Close'], facecolor='green', interpolate=True, alpha=0.3)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_xticks(data['Date'][::n])
    ax.legend()
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
    st.pyplot(fig)
# Function to create Price Changes Histogram plot
def plot_price_changes_histogram(data, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    daily_changes = data['Close'].pct_change().dropna()
    sns.histplot(daily_changes, bins=30, kde=True)
    ax.set_title(title)
    ax.set_xlabel('Daily Price Change (%)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

# Function to create Rolling Average plot
def plot_rolling_average(data, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    sampled_data = data.sample(5)  # Sample 5 dates for better readability
    rolling_avg = sampled_data['Close'].rolling(window=30).mean()  # 30-day rolling average
    ax.plot(sampled_data['Date'], sampled_data['Close'], label='Close Price', marker='o', alpha=0.5)
    ax.plot(sampled_data['Date'], rolling_avg, label='30-Day Rolling Average', color='red')
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_xticks(sampled_data['Date'])
    ax.legend()
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
    st.pyplot(fig)

# Function to create Volume vs Close Price Scatter plot
def plot_volume_price_scatter(data, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(data['Volume'], data['Close'], alpha=0.5)
    ax.set_title(title)
    ax.set_xlabel('Volume')
    ax.set_ylabel('Close Price')
    ax.set_xscale('log')  # Log scale for better visualization
    ax.set_yscale('log')
    st.pyplot(fig)

# Function to create Correlation Heatmap
def plot_correlation_heatmap(data, title):
    fig, ax = plt.subplots(figsize=(10, 8))
    corr_matrix = data.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    ax.set_title(title)
    st.pyplot(fig)

# Function to create Regression plot
def plot_regression(data, title, x_col, y_col):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='Open', y='Close', data=data, scatter_kws={'alpha': 0.5})
    ax.set_title(title)
    st.pyplot(fig)

# Function to create Residual plot
def plot_residuals(data, title, x_col, y_col):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.residplot(x='Open', y='Close', data=data, scatter_kws={'alpha': 0.5})
    ax.set_title(title)
    st.pyplot(fig)

# Function to create Average Closing Price by Year bar plot
def plot_avg_closing_price_by_year(data, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    data['Year'] = pd.to_datetime(data['Date']).dt.year
    avg_closing_price_by_year = data.groupby('Year')['Close'].mean().reset_index()
    sns.barplot(x='Year', y='Close', data=avg_closing_price_by_year, palette='viridis')
    ax.set_title(title)
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Closing Price')
    st.pyplot(fig)

# Function to create Total Volume by Month bar plot
def plot_total_volume_by_month(data, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    data['Month'] = pd.to_datetime(data['Date']).dt.month
    total_volume_by_month = data.groupby('Month')['Volume'].sum().reset_index()
    sns.barplot(x='Month', y='Volume', data=total_volume_by_month, palette='muted')
    ax.set_title(title)
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Volume')
    st.pyplot(fig)

# Function to create Maximum High Price by Year bar plot
def plot_max_high_price_by_year(data, title):
    # Check if 'Year' column exists, create it otherwise
    if 'Year' not in data.columns:
        data['Year'] = pd.to_datetime(data['Date']).dt.year

    try:
        max_high_price_by_year = data.groupby('Year')['High'].max().reset_index()

        # Create a Matplotlib figure explicitly
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Year', y='High', data=max_high_price_by_year, palette='dark', ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Year')
        ax.set_ylabel('Maximum High Price')

        # Pass the figure to st.pyplot()
        st.pyplot(fig)

    except KeyError:
        st.warning("No data available for the selected visualization.")




st.title("Cryptocurrency Dashboard")

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
    'Price Changes Histogram',
    'Rolling Average Plot',
    'Volume vs Close Price Scatter Plot',
    'Correlation Heatmap',
    'Line Chart',
    'Candlestick Chart',
    'Regression Plot',
    'Residual Plot',
    'Average Closing Price by Year',
    'Total Volume by Month',
    'Maximum High Price by Year',
])

if selected_data is not None:
    st.subheader(selected_function)
    
    # Add your function calls here based on the selected visualization
    if selected_function == 'Line Chart':
        plot_line_chart(selected_data, f'{coin_selection} - {selected_function}')
    elif selected_function == 'Candlestick Chart':
        plot_candlestick(selected_data, f'{coin_selection} - {selected_function}')
    elif selected_function == 'Price Changes Histogram':
        # Call the corresponding function from data_visual.ipynb
        plot_price_changes_histogram(selected_data, f'{coin_selection} - {selected_function}')
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
        plot_regression(selected_data, f'{coin_selection} - {selected_function}','Open', 'Close')
    elif selected_function == 'Residual Plot':
        # Call the corresponding function from data_visual.ipynb
        plot_residuals(selected_data, f'{coin_selection} - {selected_function}','Open', 'Close')
    elif selected_function == 'Average Closing Price by Year':
        plot_avg_closing_price_by_year(selected_data, f'{coin_selection} - {selected_function}')
    elif selected_function == 'Total Volume by Month':
        plot_total_volume_by_month(selected_data, f'{coin_selection} - {selected_function}')
    elif selected_function == 'Maximum High Price by Year':
        plot_max_high_price_by_year(selected_data, f'{coin_selection} - {selected_function}')
