import io
import streamlit as st
import pandas as pd

# Load your pre-trained model with OneHotEncoder inside the pipeline
model = pd.read_pickle("../../model/churn_model.pkl")  # Update path to your model file

# Streamlit app
st.title('Churn Prediction App')

st.markdown('**Please insert the user details**')


# Input fields ('User' not used in the prediction)
user_name = st.text_input('User')
credit_score = st.number_input('Credit Score', min_value=0, max_value=850, value=600)
age = st.number_input('Age', min_value=18, max_value=100, value=30)
tenure = st.number_input('Tenure (years)', min_value=0, max_value=10, value=1)
balance = st.number_input('Balance', min_value=0, value=5000)
num_of_products = st.number_input('Number of Products', min_value=1, max_value=4, value=1)
geography = st.selectbox('Geography', ['France', 'Germany', 'Spain'])  # Adjust based on your dataset
gender = st.selectbox('Gender', ['Male', 'Female'])  # Adjust based on your dataset
has_cr_card = st.selectbox('Has Credit Card', ['Yes', 'No'])
is_active_member = st.selectbox('Is Active Member', ['Yes', 'No'])
estimated_salary = st.number_input('Estimated Salary', min_value=0, value=50000)

# More user-friendly input for binary fields
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
    # Convert input data into a DataFrame
    input_df = pd.DataFrame([input_data])

    # Predict churn probability
    churn_prob = model['model'].predict_proba(input_df)[:, 1]

    # Display the result in percentage with larger text
    st.markdown(f"<h3>Churn Probability: {churn_prob[0] * 100:.2f}%</h3>", unsafe_allow_html=True)

    # Create the downloadable report
    report = input_df.copy()
    report['Churn Probability'] = churn_prob[0] * 100
    report['User'] = user_name

    # Convert report to CSV in memory using BytesIO
    csv = io.BytesIO()
    report.to_csv(csv, index=False)
    csv.seek(0)  # Move cursor back to the start so the file can be read

    # Create a downloadable button with user's name in the file name
    file_name = f"churn_prediction_report_{user_name}.csv" if user_name else "churn_prediction_report.csv"

    st.download_button(
        label="Download Report",
        data=csv,
        file_name=file_name,
        mime="text/csv"
    )