# Wine Quality Prediction

This is a simple Streamlit web application for predicting the quality of wine based on its features. It uses a machine learning model to make predictions.

## Prerequisites

Before running the application, you'll need the following:
- Python (3.6 or higher)
- Required Python packages (install using `pip install -r requirements.txt`)

## Install the required packages:

```
pip install -r requirements.txt
```

## Usage

To run the Wine Quality Prediction App, use the following command:

```
streamlit run app.py
```

This will start the Streamlit app locally, and you can access it in your web browser.

## Demo

Here's a brief overview of how the Wine Quality Prediction App works:

- The app allows users to adjust various wine features using sliders.
- Users can select different values for features like fixed acidity, volatile acidity, citric acid, etc.
- Clicking the "Predict Quality" button will use the machine learning model to predict whether the wine quality is = - "Good" or "Not Good."
- The app displays the prediction result and a quality distribution chart.
