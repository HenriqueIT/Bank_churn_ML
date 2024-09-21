# %%

import pandas as pd
import mlflow.sklearn
from mlflow import MlflowClient

data_path = "../../data/Churn_Modelling.csv"
df_teste = pd.read_csv(data_path)

# model = pd.read_pickle("../../model/churn_model.pkl")
# print(model['features'])
# pred_prob = model['model'].predict_proba(df_teste[model['features']])
# prob_churn = pred_prob[:, 1]
# df_teste['prob_churn'] = prob_churn

mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

# Set model version alias
model_name = "churn-model"
model_version = "production"
# %%

# Load the model from the Model Registry
model_uri = f"models:/{model_name}/{model_version}"
model = mlflow.sklearn.load_model(model_uri)
print(model)

# %%

model_info = mlflow.models.get_model_info(model_uri)
