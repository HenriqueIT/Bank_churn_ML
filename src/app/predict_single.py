import streamlit as st
import pandas as pd
from utils import load_model

# Function for the single prediction page
def single_prediction_page():
    # Load your pre-trained model with OneHotEncoder inside the pipeline
    model = load_model()

    st.title('Churn Prediction App')

    # Input fields ('User' not used in the prediction)
    credit_score = st.number_input('Credit Score', value=600)
    age = st.number_input('Age', value=30)
    tenure = st.number_input('Tenure (years)', min_value=0, value=1)
    balance = st.number_input('Balance', min_value=0, value=50000)
    num_of_products = st.number_input('Number of Products', value=1)
    geography = st.selectbox('Geography', ['France', 'Germany', 'Spain'])
    gender = st.selectbox('Gender', ['Male', 'Female'])
    has_cr_card = st.selectbox('Has Credit Card', ['Yes', 'No'])
    is_active_member = st.selectbox('Is Active Member', ['Yes', 'No'])
    estimated_salary = st.number_input('Estimated Salary', min_value=0, value=100000)

    # Read the data to get the average
    #data = pd.read_csv("../../data/Churn_Modelling.csv")
    data = pd.read_csv("data/Churn_Modelling.csv")

    average_credit_score = round(data.loc[data['Geography'] == geography]['CreditScore'].mean(), 1)
    average_balance = round(data.loc[data['Geography'] == geography]['Balance'].mean(), 1)
    average_num_of_products = round(data.loc[data['Geography'] == geography]['NumOfProducts'].mean(), 1)
    average_estimated_salary = round(data.loc[data['Geography'] == geography]['EstimatedSalary'].mean(), 1)

    # Convert binary inputs to numeric
    has_cr_card = 1 if has_cr_card == 'Yes' else 0
    is_active_member = 1 if is_active_member == 'Yes' else 0

    # Prepare input data
    input_data = {
        'CreditScore': credit_score,
        'Age': age,
        'Tenure': tenure,
        'Balance': balance,
        'NumOfProducts': num_of_products,
        'Geography': geography,
        'Gender': gender,
        'HasCrCard': has_cr_card,
        'IsActiveMember': is_active_member,
        'EstimatedSalary': estimated_salary
    }

    # Add a 'Check' button
    if st.button('Check'):
        input_df = pd.DataFrame([input_data])

        # Predict churn probability
        churn_prob = model['model'].predict_proba(input_df)[:, 1]

        # Display result
        st.header("Result", divider=True)
        st.markdown(f"<h5>Churn Probability: {churn_prob[0] * 100:.1f}%</h5>", unsafe_allow_html=True)

        # Compare with averages and show details
        st.header("Details", divider=True)
        st.markdown('''
            - This table compares **CreditScore, Balance, NumOfProducts, and EstimatedSalary** with averages.
            - The more parameters that are above average, the more valuable the customer might be for retention efforts.
        ''')

        # Create two columns for "Above Average" and "Below Average"
        col1, col2, col3, col4, col5 = st.columns(5)

        def check_above_below(value1, value2):
            return "✅" if value1 > value2 else "❌"

        # Display "Features" and "Comparison" columns
        with col1:
            st.markdown("**Features**")
            st.write("Credit Score")
            st.write("Balance")
            st.write("Num. Products")
            st.write("Estimated Salary")

        with col2:
            st.markdown("**Input**")
            st.write(credit_score)
            st.write(balance)
            st.write(num_of_products)
            st.write(estimated_salary)

        with col3:
            st.markdown(f"**Avg. in {geography}**")
            st.write(average_credit_score)
            st.write(average_balance)
            st.write(average_num_of_products)
            st.write(average_estimated_salary)

        with col4:
            st.markdown("**Above Avg.**")
            st.write(check_above_below(credit_score, average_credit_score))
            st.write(check_above_below(balance, average_balance))
            st.write(check_above_below(num_of_products, average_num_of_products))
            st.write(check_above_below(estimated_salary, average_estimated_salary))

        with col5:
            st.markdown("**Below Avg.**")
            st.write(check_above_below(average_credit_score, credit_score))
            st.write(check_above_below(average_balance, balance))
            st.write(check_above_below(average_num_of_products, num_of_products))
            st.write(check_above_below(average_estimated_salary, estimated_salary))