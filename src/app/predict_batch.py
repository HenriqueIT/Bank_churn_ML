import streamlit as st
import pandas as pd
from datetime import datetime
from utils import load_model

# Function for batch prediction
def batch_prediction_page():
    st.title("Batch Churn Prediction")

    # Instruction
    st.markdown("Upload a CSV file with the following columns to predict churn probability:")
    st.markdown(
        """
        - CreditScore
        - Geography
        - Gender
        - Age
        - Tenure
        - Balance
        - NumOfProducts
        - HasCrCard
        - IsActiveMember
        - EstimatedSalary
        """
    )

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(uploaded_file)

        # Display the uploaded data
        st.write("Uploaded Data:")
        st.dataframe(data)

        # Ensure all required columns are present
        required_columns = [
            'CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance',
            'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary'
        ]
        if all(column in data.columns for column in required_columns):
            # Load the model
            model = load_model()

            # Convert categorical columns if needed (optional)
            data['HasCrCard'] = data['HasCrCard'].apply(lambda x: 1 if x == 'Yes' else 0)
            data['IsActiveMember'] = data['IsActiveMember'].apply(lambda x: 1 if x == 'Yes' else 0)

            # Predict churn probabilities
            data['churn_prob'] = (model['model'].predict_proba(data[required_columns])[:, 1])*100

            # Display the result
            st.write("Data with Churn Probability:")
            st.dataframe(data)

            # Download the result as a CSV file
            csv = data.to_csv(index=False)
            st.download_button(
                label="Download CSV with Churn Probability",
                data=csv,
                file_name=f'churn_predictions_{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}.csv',
                mime='text/csv'
            )
        else:
            # Display an error message with the missing columns

            missing_columns = [col for col in required_columns if col not in data.columns]
            st.error(f"Missing columns in the uploaded file: {', '.join(missing_columns)}")
