import streamlit as st
import pathlib

def load_CSS(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path(__file__).parent / "assets" / "style.css"
load_CSS(css_path)

st.markdown("<h1 style='text-align: center; color: #3b82f6; margin-bottom: 50px; padding: 0;'>Sales Forecasting and Demand Prediction</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h3 style='color: #1d4ed8;'>Input Features</h3>", unsafe_allow_html=True)
    
    for i in range(3):
        col_a, col_b = st.columns(2)
        with col_a:
            feature_name = f"feature_{i*2+1}"
            globals()[feature_name] = st.text_input(f"Feature {i*2+1}", key=feature_name)
        with col_b:
            feature_name = f"feature_{i*2+2}"
            globals()[feature_name] = st.text_input(f"Feature {i*2+2}", key=feature_name)

    predict_button = st.button("Predict", type="primary")

with col2:
    st.markdown("<h3 style='color: #1d4ed8;'>Prediction Result</h3>", unsafe_allow_html=True)
    if predict_button:
        st.write("Prediction 1: ...")
        st.write("Prediction 2: ...")
        st.write("Prediction 3: ...")
        st.write("Prediction 4: ...")
        st.write("Prediction 5: ...")