import streamlit as st
import pickle
import numpy as np
import pandas as pd
import pathlib

# Set page config
st.set_page_config(page_title="Sales Prediction App", page_icon="📈", layout="wide")

# External link button
st.link_button("Sales Dashboard", "https://sales-dashboard-application.streamlit.app/")

def load_CSS(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path(__file__).parent / "assets" / "style.css"
load_CSS(css_path)

# Title
st.title("Sales Prediction Model")

# Define feature mappings
FEATURE_MAPPINGS = {
    'Order Priority': ["Critical", "High", "Medium", "Low"],
    'Ship Mode': ["Standard Class", "Second Class", "First Class", "Same Day"],
    'Market': ["US", "EU", "APAC", "LATAM", "Africa"],
    'Category': ["Furniture", "Office Supplies", "Technology"],
    'Sub-Category': ["Bookcases", "Chairs", "Tables", "Furnishings", "Paper", "Binders", 
                    "Storage", "Appliances", "Phones", "Accessories", "Machines", "Copiers"]
}

# Load model
def load_model():
    model_path = pathlib.Path(__file__).parent / "xgboost_sales_model.pkl"
    try:
        with open(model_path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

model = load_model()

# Create input form
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Numeric Features")
        quantity = st.number_input("Quantity", min_value=1, max_value=100, value=1, step=1)
        discount = st.number_input("Discount (0-1)", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
        profit = st.number_input("Profit", min_value=-1000.0, max_value=1000.0, value=0.0, step=0.01)
        shipping_cost = st.number_input("Shipping Cost", min_value=0.0, max_value=1000.0, value=0.0, step=0.01)
        
    with col2:
        st.markdown("### Date Features")
        month = st.selectbox("Month", range(1, 13), format_func=lambda x: pd.Timestamp(2020, x, 1).strftime('%B'))
        year = st.selectbox("Year", range(2014, 2018))
        day_of_week = st.selectbox("Day of Week", range(1, 8), format_func=lambda x: pd.Timestamp(2020, 1, x).strftime('%A'))
        day_of_month = st.selectbox("Day of Month", range(1, 32))
        is_weekend = st.selectbox("Is Weekend", ["Yes", "No"])
    
    with col3:
        st.markdown("### Categorical Features")
        order_priority = st.selectbox("Order Priority", FEATURE_MAPPINGS['Order Priority'])
        ship_mode = st.selectbox("Ship Mode", FEATURE_MAPPINGS['Ship Mode'])
        market = st.selectbox("Market", FEATURE_MAPPINGS['Market'])
        category = st.selectbox("Category", FEATURE_MAPPINGS['Category'])
        sub_category = st.selectbox("Sub-Category", FEATURE_MAPPINGS['Sub-Category'])
    
    submit_button = st.form_submit_button("Predict Sales")

# Handle prediction
if submit_button and model is not None:
    try:
        # Prepare features
        features = [
            quantity, discount, profit, shipping_cost,
            month, year, day_of_week,
            1 if is_weekend == "Yes" else 0,
            day_of_month,
            FEATURE_MAPPINGS['Order Priority'].index(order_priority),
            FEATURE_MAPPINGS['Ship Mode'].index(ship_mode),
            FEATURE_MAPPINGS['Market'].index(market),
            FEATURE_MAPPINGS['Category'].index(category),
            FEATURE_MAPPINGS['Sub-Category'].index(sub_category)
        ]
        
        # Make prediction
        features = np.array(features).reshape(1, -1)
        prediction = model.predict(features)[0]
        
        # Display results
        st.success("Prediction Complete!")
        st.metric("Predicted Sales", f"${prediction:,.2f}")
        
        # Show input summary
        st.subheader("Input Summary")
        summary = pd.DataFrame({
            'Feature': ['Quantity', 'Discount', 'Profit', 'Shipping Cost', 'Month', 'Year',
                        'Day of Week', 'Is Weekend', 'Day of Month', 'Order Priority',
                        'Ship Mode', 'Market', 'Category', 'Sub-Category'],
            'Value': [quantity, f"{discount:.2%}", f"${profit:,.2f}", f"${shipping_cost:,.2f}",
                        pd.Timestamp(2020, month, 1).strftime('%B'), year,
                        pd.Timestamp(2020, 1, day_of_week).strftime('%A'), is_weekend,
                        day_of_month, order_priority, ship_mode, market, category, sub_category]
        })
        st.dataframe(summary, use_container_width=True)
        st.markdown(
            """
            <style>
            .stDataFrameContainer {
                min-width: 600px !important;
                width: 100% !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")

# Sidebar information
# with st.sidebar:
#     st.header("About")
#     st.markdown("""
#     ### How to use:
#     1. Enter the values for each feature
#     2. Click the 'Predict Sales' button
#     3. View the prediction result
    
#     ### Note:
#     - Quantity: 1-100
#     - Discount: 0-1 (percentage)
#     - Profit/Shipping Cost: Any reasonable value
#     - Date features: Use dropdowns for accuracy
#     """) 