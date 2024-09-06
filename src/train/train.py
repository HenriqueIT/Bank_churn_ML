# %%
# Basic libraries
import datetime
import numpy as np
import pandas as pd

# Data processing
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.pipeline import Pipeline
from feature_engine import encoding

# Modelling
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, f1_score, precision_score, recall_score


# Read the dataset
data_path = "../../data/Churn_Modelling.csv"
df = pd.read_csv(data_path)

df.head()

# %%

# Drop unncessary columns for modelling ('RowNumber', 'CustomerId', 'Surname')
cols_drop = ['RowNumber', 'CustomerId', 'Surname']
df = df.drop(cols_drop, axis=1)

# Separate the dataset into features and target
col_features = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'Geography', 
                'Gender', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
col_target = ['Exited']

X = df[col_features]
y = df[col_target]

# %%

# Create a balanced dataset as only 20% of rows have 'Exited' = 1 (Upsampling)
X_churned = X[(y==1).values]
y_churned = y[(y==1).values]

X_upsampled, y_upsampled = resample(X_churned, y_churned, n_samples=(y['Exited']==0).sum())

X_bal = pd.concat([X[(y==0).values], X_upsampled])
y_bal = pd.concat([y[(y==0).values], y_upsampled]).to_numpy().ravel()

X_train, X_test, y_train, y_test = train_test_split(X_bal,
                                                    y_bal,                                            
                                                    train_size=0.8,
                                                    )

# %%
# Perform onehot encoding on categorical columns
col_categorical = ['Geography', 'Gender']

onehot_enc = encoding.OneHotEncoder(drop_last=True,
                                    variables= col_categorical)

forest_model = RandomForestClassifier(n_estimators= 50, 
                                      min_samples_split= 2, 
                                      max_features=5)

model_pipe = Pipeline([('one_hot_encoding', onehot_enc),
                           ('random_forest', forest_model)])

# %%
model_pipe.fit(X_train, y_train)

# %%
# Make predictions
y_pred = model_pipe.predict(X_test)
y_pred_proba = model_pipe.predict_proba(X_test)[:, 1]

# Calculate and round metrics to 4 decimal places
metrics_dict = {
    'accuracy': round(accuracy_score(y_test, y_pred), 4),
    'precision': round(precision_score(y_test, y_pred), 4),
    'recall': round(recall_score(y_test, y_pred), 4),
    'roc_auc': round(roc_auc_score(y_test, y_pred_proba), 4),
    'f1_score': round(f1_score(y_test, y_pred), 4)
}

# Print metrics
for metric, value in metrics_dict.items():
    print(f'Test {metric.capitalize()}: {value:.4f}')

model_series = pd.Series({
    "model": model_pipe,
    "features": col_features,
    "metrics": metrics_dict,
    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# %%
# Save the model to model folder
model_series.to_pickle("../../model/churn_model.pkl")

# %%
