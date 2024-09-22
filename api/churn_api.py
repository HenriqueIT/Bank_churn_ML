from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd

# Initialize the FastAPI app
app = FastAPI()

# Load your pre-trained model
# model = pd.read_pickle("../model/churn_model.pkl")
model = pd.read_pickle("model/churn_model.pkl")

# Define a Pydantic model for input validation with an example
class ChurnInput(BaseModel):
    CreditScore: int = Field(..., example=700)
    Age: int = Field(..., example=35)
    Tenure: int = Field(..., example=2)
    Balance: float = Field(..., example=15000.75)
    NumOfProducts: int = Field(..., example=2)
    Geography: str = Field(..., example="France")
    Gender: str = Field(..., example="Male")
    HasCrCard: int = Field(..., example=1) 
    IsActiveMember: int = Field(..., example=1)
    EstimatedSalary: float = Field(..., example=60000.00)

# Define the POST method for churn prediction
@app.post("/predict/")
def predict_churn(input_data: ChurnInput):
    # Convert input data into a dictionary
    input_dict = input_data.dict()

    # Convert dictionary to DataFrame (the model expects a DataFrame)
    input_df = pd.DataFrame([input_dict])

    # Predict churn probability
    churn_prob = model['model'].predict_proba(input_df)[:, 1]

    # Return the result as JSON
    return {"churn_probability": churn_prob[0]}
