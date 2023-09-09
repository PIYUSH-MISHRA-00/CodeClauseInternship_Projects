import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Load the quality prediction model
quality_model = pickle.load(open("model/quality_model.pkl", "rb"))

# Streamlit UI
st.title("Wine Quality Prediction App")

st.header("Quality Prediction")

# Input sliders for wine features
fixed_acidity = st.slider("Fixed Acidity:", 4.0, 15.9, 8.0, 0.1)
volatile_acidity = st.slider("Volatile Acidity:", 0.12, 1.58, 0.5, 0.01)
citric_acid = st.slider("Citric Acid:", 0.0, 1.0, 0.5, 0.01)
residual_sugar = st.slider("Residual Sugar:", 0.9, 15.5, 2.0, 0.1)
chlorides = st.slider("Chlorides:", 0.01, 0.6, 0.08, 0.01)
free_sulfur_dioxide = st.slider("Free Sulfur Dioxide:", 1, 72, 20, 1)
total_sulfur_dioxide = st.slider("Total Sulfur Dioxide:", 6, 289, 100, 1)
density = st.slider("Density:", 0.99, 1.01, 1.0, 0.001)
pH = st.slider("pH:", 2.74, 4.01, 3.0, 0.01)
sulphates = st.slider("Sulphates:", 0.33, 2.0, 0.6, 0.01)
alcohol = st.slider("Alcohol:", 8.4, 14.9, 11.0, 0.1)

if st.button("Predict Quality"):
    # Prepare input data for prediction
    input_data = np.array([[
        fixed_acidity, volatile_acidity, citric_acid, 
        residual_sugar, chlorides, free_sulfur_dioxide, 
        total_sulfur_dioxide, density, pH, sulphates, alcohol
    ]])

    # Use the quality prediction model to make predictions
    quality_prediction = quality_model.predict(input_data)[0]
    
    # Determine and display the prediction result
    if quality_prediction == 1:
        result_text = "Predicted Quality: Good"
    else:
        result_text = "Predicted Quality: Not Good"
    
    st.write(result_text)

    # Quality distribution chart
    st.subheader("Quality Distribution")
    quality_counts = quality_model.predict(np.random.rand(1000, 11))
    plt.hist(quality_counts, bins=[0, 1, 2], align='left', rwidth=0.6)
    plt.xticks([0, 1], ["Not Good", "Good"])
    plt.xlabel("Quality")
    plt.ylabel("Count")
    st.pyplot(plt)
