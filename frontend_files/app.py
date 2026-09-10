import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860" # Keep this as 'http://backend:7860' for Docker network communication

# Set the title of the Streamlit app
st.title("SuperKart Product Revenue Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for product features, matching the model's expected inputs
product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66, step=0.01)
product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027, step=0.001, format="%.3f")
product_mrp = st.number_input("Product MRP", min_value=0.0, value=117.08, step=0.01)
store_age_years = st.number_input("Store Age (Years)", min_value=0, value=16)
store_id = st.selectbox("Store ID", ['OUT004', 'OUT001', 'OUT003', 'OUT002'])
store_size = st.selectbox("Store Size", ["Medium", "High", "Small"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 2", "Tier 1", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type2", "Departmental Store", "Supermarket Type1", "Food Mart"])
product_id_type = st.selectbox("Product ID Type", ["FD", "NC", "DR"])
food_type = st.selectbox("Food Type", ["Perishable", "Non Perishable"])

# Convert user input into a dictionary for the API payload
payload = {
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_MRP': product_mrp,
    'Store_Age_Years': store_age_years,
    'Store_Id': store_id,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'Product_Id_char': product_id_type,
    'Product_Type_Category': food_type
}

# Make prediction when the "Predict" button is clicked
if st.button("Predict Product Revenue", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/productRevenue", json=payload)  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted_Sales']
        st.success(f"Predicted Product Sales: {prediction:.2f}")
    else:
        st.error(f"Unable to connect to the prediction API. Status Code: {response.status_code}, Response: {response.text}")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch from CSV", type="primary"):
        files = {"file": uploaded_file.getvalue()} # Get the bytes content of the uploaded file
        response = requests.post(f"{BACKEND_URL}/v1/productRevenueBatch", files=files)  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            # Display predictions, assuming they are in a list format
            st.write(pd.DataFrame(predictions['Batch_Predictions'], columns=['Predicted Sales']))
        else:
            st.error(f"Unable to connect to the prediction API for batch. Status Code: {response.status_code}, Response: {response.text}")
