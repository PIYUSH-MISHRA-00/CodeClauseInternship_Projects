import pandas as pd
import streamlit as st
import pickle

# Load the dataset
df = pd.read_excel(r'E:\Internship_Projects\CodeClauseInternship_Projects\Recommendation System for Retail Stores\dataset\Online Retail.xlsx')

# Load the item-item similarity matrix from pickle
with open(r'E:\Internship_Projects\CodeClauseInternship_Projects\Recommendation System for Retail Stores\model\item_item_sim_matrix.pkl', 'rb') as pickle_file:
    item_item_sim_matrix = pickle.load(pickle_file)

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
                top_similar_items = list(item_item_sim_matrix.loc[item].sort_values(ascending=False).iloc[:10].index)
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
