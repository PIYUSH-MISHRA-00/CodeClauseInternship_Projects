import pandas as pd
import streamlit as st
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import h5py

# Load the dataset
df = pd.read_excel(r'E:\Internship_Projects\CodeClauseInternship_Projects\Recommendation System for Retail Stores\dataset\Online Retail.xlsx')

# Calculate the item-item similarity matrix
def calculate_similarity_matrix(df):
    # Pivot table
    customer_item_matrix = df.pivot_table(
        index='CustomerID',
        columns='StockCode',
        values='Quantity',
        aggfunc='sum'
    ).fillna(0)

    # Calculate cosine similarity
    item_item_sim_matrix = cosine_similarity(customer_item_matrix.T)

    return item_item_sim_matrix

# Load or calculate the similarity matrix
try:
    # Try to load the matrix from HDF5 file
    with h5py.File('item_item_sim_matrix.h5', 'r') as h5f:
        item_item_sim_matrix = h5f['item_item_sim_matrix'][:]
except (FileNotFoundError, KeyError):
    item_item_sim_matrix = calculate_similarity_matrix(df)
    # Save the similarity matrix in HDF5 format
    with h5py.File('item_item_sim_matrix.h5', 'w') as h5f:
        h5f.create_dataset('item_item_sim_matrix', data=item_item_sim_matrix)

# Convert the similarity matrix to a sparse matrix
item_item_sim_matrix_sparse = csr_matrix(item_item_sim_matrix)

# Streamlit app
st.title("Recommendation for Retail Store App")

# Sidebar for user-based recommendations
st.sidebar.title("User-Based Recommendations")
user_id = st.sidebar.text_input("Enter User ID:")

# Sidebar for searching products
st.sidebar.title("Product Search")
search_term = st.sidebar.text_input("Search for Products:")

if user_id:
    try:
        user_id = int(user_id)
        if user_id in df['CustomerID'].unique():
            # User-based recommendation
            st.sidebar.write("User-based recommendations for User ID:", user_id)
            user_items = df.loc[df['CustomerID'] == user_id, 'StockCode'].unique()
            recommended_items = []

            for item in user_items:
                top_similar_items = list(item_item_sim_matrix_sparse[item].toarray().flatten().argsort()[::-1][:10])
                recommended_items.extend(top_similar_items)

            recommended_items = list(set(recommended_items) - set(user_items))
            recommended_products = df.loc[df['StockCode'].isin(recommended_items), ['StockCode', 'Description']].drop_duplicates().set_index('StockCode')
            st.write("Recommended Products:")
            st.table(recommended_products)

        else:
            st.sidebar.error("User not found. Please enter a valid User ID.")
    except ValueError:
        st.sidebar.error("Invalid input. Please enter a valid User ID.")

if search_term:
    # Product search functionality
    filtered_products = df[df['Description'].str.contains(search_term, case=False, na=False)]
    st.sidebar.write("Search results for:", search_term)
    st.table(filtered_products[['StockCode', 'Description']])

# Display the dataset
if st.checkbox("Show Dataset"):
    st.write(df)

# Additional features and visualizations can be added as needed.
