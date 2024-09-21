import streamlit as st
from predict_single import single_prediction_page
from predict_batch import batch_prediction_page

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["Single Prediction", "Batch Prediction"])

# Display the selected page
if page == "Single Prediction":
    single_prediction_page()
elif page == "Batch Prediction":
    batch_prediction_page()