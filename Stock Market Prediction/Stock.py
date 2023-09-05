import streamlit as st
import pandas as pd
import pickle
import yfinance as yf
import matplotlib.pyplot as plt
import random
import time
import os
from sklearn.impute import SimpleImputer
import plotly.graph_objs as go 

# Load the trained model from the pickle file
with open('model\stock_price_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Streamlit app
st.title('Stock Analysis and Prediction App')

# Create a menu for user options
selected_option = st.sidebar.selectbox('Select an Option', ('Stock Analysis', 'Live Data Analysis', 'CSV Viewer'))

# Function to get stock data by name (you need a dataset with stock names)
def get_stock_data(stock_name):
    # Load historical stock data for the given stock name using yfinance
    stock_data = yf.download(stock_name, period="1y")
    return stock_data

if selected_option == 'Stock Analysis':
    st.header('Stock Analysis by Name')
    
    # Input for user to enter a stock name
    stock_name = st.text_input('Enter a stock symbol (e.g., AAPL for Apple Inc.):')

    if st.button('Submit'):  # Add a Submit button to trigger the analysis
        # Display stock data
        if stock_name:
            stock_data = get_stock_data(stock_name)
            if not stock_data.empty:
                st.write(f'Displaying historical data for {stock_name}:')
                st.write(stock_data)
                
                # Add a line chart for stock data visualization
                plt.figure(figsize=(10, 6))
                plt.plot(stock_data.index, stock_data['Close'], label='Close Price')
                plt.xlabel('Date')
                plt.ylabel('Close Price')
                plt.title(f'{stock_name} Stock Price Analysis')
                st.pyplot(plt)  # Display the plot in Streamlit
                
                # Add more visualizations or analysis here
            else:
                st.write(f'No data available for {stock_name}.')


elif selected_option == 'Live Data Analysis':
    st.header('Live Data Analysis and Prediction')
    
    # Input for user to enter a stock symbol for live data analysis
    live_stock_symbol = st.text_input('Enter a stock symbol (e.g., AAPL for Apple Inc.) for live data analysis:')

    # Fetch real-time stock data using yfinance
    live_stock_data = yf.Ticker(live_stock_symbol)
    
    # Check if the stock symbol is valid and data is available
    if live_stock_data.history(period="1d").empty:
        st.write('Invalid stock symbol or no data available.')
    else:
        # Display real-time stock data
        st.write(f'Real-time data for {live_stock_symbol}:')
        st.write(live_stock_data.history(period="1d"))
        
        # Input for user to enter live opening price
        live_open_price = st.number_input('Enter live opening price for prediction:')

        # Check if the model is loaded
        if 'model/stock_price_model.pkl' in os.listdir():
            # Load the trained model using pickle
            with open('model/stock_price_model.pkl', 'rb') as model_file:
                model = pickle.load(model_file)
                
            # Predict the live closing price using the model
            live_predicted_close = model.predict([[live_open_price]])[0]
            
            # Display the predicted closing price for live data
            st.write(f'Predicted Live Closing Price: {live_predicted_close:.2f}')
            
            # Real-time price chart
            live_stock_data = live_stock_data.history(period="1d")
            fig = go.Figure(data=[go.Candlestick(x=live_stock_data.index,
                                                open=live_stock_data['open'],
                                                high=live_stock_data['high'],
                                                low=live_stock_data['low'],
                                                close=live_stock_data['close'])])
            st.plotly_chart(fig)
            
            
elif selected_option == 'CSV Viewer':
    st.header('CSV Viewer')

    # Input for user to upload a CSV file
    uploaded_file = st.file_uploader("Upload a CSV file:", type=["csv"])

    if uploaded_file is not None:
        # Load the uploaded CSV data
        user_data = pd.read_csv(uploaded_file)

        # Display the user-provided data
        st.write("User-Provided Data:")
        st.write(user_data)

        # Allow users to select columns for visualization
        selected_columns = st.multiselect("Select columns for visualization:", user_data.columns)

        if selected_columns:
            # Create a Plotly figure to visualize selected columns
            fig = go.Figure()

            for column in selected_columns:
                fig.add_trace(go.Scatter(x=user_data.index, y=user_data[column], name=column))

            fig.update_layout(
                title=f"Visualization of {', '.join(selected_columns)}",
                xaxis_title="Timestamp",
                yaxis_title="Value",
                xaxis_rangeslider_visible=True,
            )

            st.plotly_chart(fig)
        else:
            st.write("Please select one or more columns for visualization.")
    else:
        st.write("Please upload a CSV file to view its contents.")

