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

    # Explanation of 'profitable_customer'
    st.markdown(
        """
        ### Profitable Customer Explanation:
        A customer is considered **'profitable'** if any of the following values exceed the average for the customer's country:
        - **CreditScore**
        - **Balance**
        - **Number of Products**
        - **Estimated Salary**
        
        These averages are calculated based on historical data from other customers within the same country (Geography).
        If any one of these values is higher than the corresponding country's average, the customer will be marked with "✅" in the **profitable_customer column**.
        """
    )

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(uploaded_file)

        # Read the data to get the average of credit score
        # balance, num of products and salary for each country
        # data_avg = pd.read_csv("../../data/Churn_Modelling.csv")
        data_avg = pd.read_csv("data/Churn_Modelling.csv")

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

            # Predict churn probabilities
            data['churn_prob'] = (model['model'].predict_proba(data[required_columns])[:, 1])*100

            # Calculate average values for each Geography
            averages = data_avg.groupby('Geography').agg({
                'CreditScore': 'mean',
                'Balance': 'mean',
                'NumOfProducts': 'mean',
                'EstimatedSalary': 'mean'
            }).reset_index()

            # Merge the input data with averages based on Geography
            data = data.merge(averages, on='Geography', suffixes=('', '_avg'))

            # Predict churn probabilities
            data['churn_probability'] = (model['model'].predict_proba(data[required_columns])[:, 1]) * 100

            # Create 'profitable_customer' column
            data['profitable_customer'] = (
                (data['CreditScore'] > data['CreditScore_avg']) |
                (data['Balance'] > data['Balance_avg']) |
                (data['NumOfProducts'] > data['NumOfProducts_avg']) |
                (data['EstimatedSalary'] > data['EstimatedSalary_avg'])
            )

            data = data.round({"CreditScore_avg":1, "Balance_avg":1, "NumOfProducts_avg":1, "EstimatedSalary_avg":1}) 


            # Display the result
            st.write("Data with churn_probability and profitable_customer column:")
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
