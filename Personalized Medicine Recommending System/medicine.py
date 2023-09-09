import os
import streamlit as st
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Define the folder where you want to save the PDFs
pdf_folder = "pdf"  # You can change this to your desired folder name

# Ensure the folder exists; create it if it doesn't
os.makedirs(pdf_folder, exist_ok=True)

st.title("Personalized Medicine Recommendations")

# Load the recommendation model from the pickle file
with open(r"model/medicine_recommendation_model.pkl", "rb") as model_file:
    tfidf_vectorizer, tfidf_matrix = pickle.load(model_file)

# Create a DataFrame or load the dataset that contains drug names and conditions
# Replace 'your_dataset.csv' with the actual file path or URL of your dataset
df = pd.read_csv(r'datasets\drugsComTest_raw.csv')

user_condition = st.text_input("Enter your health condition:")

if user_condition:
    user_condition_tfidf = tfidf_vectorizer.transform([user_condition])
    similarity_scores = cosine_similarity(user_condition_tfidf, tfidf_matrix)
    
    top_indices = similarity_scores.argsort()[0][::-1][:10]  # Select top 10 indices
    top_medicines = df['drugName'].iloc[top_indices]
    
    st.write("Top 10 recommended medicines for", user_condition, ":")
    st.write(top_medicines.tolist())
    
    # Generate a PDF report with problem name and related medicines
    if st.button("Generate PDF Report"):
        # Create the PDF folder if it doesn't exist
        os.makedirs(pdf_folder, exist_ok=True)
        
        # Define the PDF file path
        pdf_filename = os.path.join(pdf_folder, f"{user_condition}_recommendations.pdf")
        
        # Create a PDF report
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, "Personalized Medicine Recommendations")
        c.drawString(100, 730, f"Health Condition: {user_condition}")
        
        y = 700
        for i, medicine in enumerate(top_medicines.tolist(), start=1):
            y -= 20
            c.drawString(100, y, f"{i}. {medicine}")
        
        c.save()
        
        # Provide a download link for the PDF
        st.write(f"Download the PDF report: [Download PDF]({pdf_filename})")
