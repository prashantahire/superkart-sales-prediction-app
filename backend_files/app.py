import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app with a name for SuperKart Sales Predictor
superkart_sales_predictor_api = Flask("SuperKart Sales Predictor")

# Load the trained sales prediction model
model = joblib.load("superkart_model_v1_0.joblib")

# Define a route for the home page
@superkart_sales_predictor_api.get('/')
def home():
    return "Welcome to the SuperKart Sales Predictor API!"

# Define an endpoint to predict sales for a single product
@superkart_sales_predictor_api.post('/v1/productRevenue')
def predict_product_revenue():
    # Get JSON data from the request
    product_data = request.get_json()

    # Extract relevant product features from the input data
    # These features must match those used during model training
    sample = {
        'Product_Weight': product_data['Product_Weight'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_MRP': product_data['Product_MRP'],
        'Store_Age_Years': product_data['Store_Age_Years'],
        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
        'Store_Type': product_data['Store_Type'],
        'Store_Id': product_data['Store_Id'], # Added Store_Id
        'Product_Id_Type': product_data['Product_Id_Type'], # Corrected from Product_Id_char
        'Food_Type': product_data['Food_Type'] # Corrected from Product_Type_Category
    }

    # Convert the extracted data into a DataFrame
    input_df = pd.DataFrame([sample])

    # Make a sales prediction using the trained model
    prediction = model.predict(input_df).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Predicted_Sales': prediction})

# Define an endpoint to predict sales for a batch of products
@superkart_sales_predictor_api.post('/v1/productRevenueBatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    batch_input_df = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(batch_input_df).tolist()

    # Assuming the input CSV has an 'index' or unique identifier that can be used
    # If not, we can just return a list of predictions
    # For this example, let's assume the rows are implicitly indexed by their order.
    return jsonify({'Batch_Predictions': predictions})

# Run the Flask app in debug mode
if __name__ == '__main__':
    superkart_sales_predictor_api.run(debug=True)
