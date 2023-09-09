![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)

# Personalized Medicine Recommendation App

The Personalized Medicine Recommendation App is a Python-based web application that provides personalized medicine recommendations based on the user's health condition. It uses natural language processing techniques to match user-provided health conditions with relevant medicines.

## Features

- Users can input their health condition.
- The app recommends the top 10 medicines related to the provided health condition.
- Users can generate and download a PDF report with the recommended medicines.
- PDF reports are saved in a designated folder.

## Getting Started

### Prerequisites

To run this application, you need the following:

- Python (3.7 or higher)
- pip (Python package manager)

### Installation

Install the required Python packages:
```
pip install -r requirements.txt
```
## Usage

Run the Streamlit app:
```
streamlit run medicine.py
```

- Access the app in your web browser.

- Enter your health condition in the provided text input field.

- Click the "Generate Recommendations" button to view the top 10 recommended medicines.

- To generate and download a PDF report, click the "Generate PDF Report" button.
