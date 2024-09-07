# %%

import pandas as pd

data_path = "../../data/Churn_Modelling.csv"
df_teste = pd.read_csv(data_path)

model = pd.read_pickle("../../model/churn_model.pkl")
# %%

pred_prob = model['model'].predict_proba(df_teste[model['features']])
prob_churn = pred_prob[:, 1]
prob_churn

# %%