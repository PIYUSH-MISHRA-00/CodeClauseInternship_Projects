import streamlit as st
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the quality and price prediction models
quality_model = pickle.load(open("quality_model.pkl", "rb"))
price_model = pickle.load(open("price_model.pkl", "rb"))

# Streamlit UI
st.title("Wine Quality and Price Prediction App")

# Sidebar menu to select prediction type
selected_option = st.sidebar.selectbox("Select prediction type:", ["Quality Prediction", "Price Prediction", "Feature Comparison", "Predict from CSV"])

if selected_option == "Quality Prediction":
    st.header("Quality Prediction")
    # Input fields for quality prediction
    # Replace with relevant feature input fields (e.g., Rating, NumberOfRatings, etc.)
    rating = st.number_input("Enter Rating:")
    num_of_ratings = st.number_input("Enter Number of Ratings:")

    if st.button("Predict Quality"):
        # Use the quality prediction model to make predictions
        quality_prediction = quality_model.predict([[rating, num_of_ratings]])[0]
        st.write(f"Predicted Quality: {quality_prediction:.2f}")

        # Pie chart for quality distribution
        quality_counts = [0, 0, 0]  # Replace with actual counts for different quality levels
        labels = ["Low", "Medium", "High"]
        fig, ax = plt.subplots()
        ax.pie(quality_counts, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

elif selected_option == "Price Prediction":
    st.header("Price Prediction")
    # Input fields for price prediction
    # Replace with relevant feature input fields (e.g., Country, Region, etc.)
    country = st.text_input("Enter Country:")
    region = st.text_input("Enter Region:")

    if st.button("Predict Price"):
        # Use the price prediction model to make predictions
        price_prediction = price_model.predict([[country, region]])[0]
        st.write(f"Predicted Price: {price_prediction:.2f}")

        # Pie chart for price range distribution
        price_ranges = [0, 0, 0]  # Replace with actual counts for different price ranges
        labels = ["Low", "Medium", "High"]
        fig, ax = plt.subplots()
        ax.pie(price_ranges, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

elif selected_option == "Feature Comparison":
    st.header("Feature Comparison")
    # User input for two wine samples for feature comparison
    # Replace with input fields for selecting two wine samples

    # Display a table comparing the selected features of two wine samples
    # Replace with code to compare selected features

    # Pie chart showing the distribution of wine qualities for the selected samples
    # Replace with code for creating a pie chart

    # Explanation
    st.subheader("Explanation")
    st.write("You can use this section to compare the features of two wine samples and visualize the distribution of wine qualities for the selected samples.")

elif selected_option == "Predict from CSV":
    st.header("Predict from CSV")
    # Input for user to upload a CSV file with wine parameters
    uploaded_file = st.file_uploader("Upload a CSV file with wine parameters:", type=["csv"])

    if uploaded_file is not None:
        user_data = pd.read_csv(uploaded_file)
        user_quality_predictions = user_data.apply(lambda row: quality_model.predict([row])[0], axis=1)
        user_price_predictions = user_data.apply(lambda row: price_model.predict([row])[0], axis=1)
        user_data["Predicted Quality"] = user_quality_predictions
        user_data["Predicted Price"] = user_price_predictions

        st.write("User-Provided Data with Predictions:")
        st.write(user_data)

        # Pie chart for quality distribution
        quality_counts = user_data["Predicted Quality"].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(quality_counts, labels=quality_counts.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

        # Pie chart for price range distribution
        price_ranges = user_data["Predicted Price"].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(price_ranges, labels=price_ranges.index, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)

        # Explanation
        st.subheader("Explanation")
        st.write("You can upload a CSV file with wine parameters, and the app will predict both quality and price for each entry in the file. The predictions are visualized with pie charts.")
