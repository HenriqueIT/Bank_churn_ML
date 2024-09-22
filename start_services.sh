#!/bin/sh

# Start FastAPI in the background
uvicorn api.churn_api:app --host 0.0.0.0 --port 8000 &

# Start Streamlit
streamlit run src/app/app.py --server.port 8501 --server.address 0.0.0.0