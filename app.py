import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Optional: train a simple model using dummy data
@st.cache_resource
def train_model():
    # Example dataset (mock data for demo)
    data = {
        'age': [25, 32, 47, 51, 62],
        'sex': [1, 0, 1, 0, 1],  # 1 = male, 0 = female
        'bmi': [22.2, 28.5, 30.1, 26.3, 31.5],
        'children': [0, 1, 3, 2, 0],
        'smoker': [0, 1, 0, 1, 0],
        'region': [0, 1, 2, 1, 3],  # 0-3 representing regions
        'charges': [2000, 15000, 12000, 18000, 13000]
    }
    df = pd.DataFrame(data)
    X = df.drop('charges', axis=1)
    y = df['charges']
    model = LinearRegression()
    model.fit(X, y)
    return model

model = train_model()

st.title("🏥 Health Insurance Premium Prediction")

# Input form
age = st.number_input("Age", 18, 100, step=1)
sex = st.selectbox("Sex", ["Male", "Female"])
bmi = st.number_input("BMI", 10.0, 50.0)
children = st.number_input("Number of Children", 0, 10, step=1)
smoker = st.selectbox("Smoker", ["Yes", "No"])
region = st.selectbox("Region", ["Northeast", "Northwest", "Southeast", "Southwest"])

# Encode inputs
sex_val = 1 if sex == "Male" else 0
smoker_val = 1 if smoker == "Yes" else 0
region_val = {"Northeast": 0, "Northwest": 1, "Southeast": 2, "Southwest": 3}[region]

# Prediction
if st.button("Predict Premium"):
    input_data = np.array([[age, sex_val, bmi, children, smoker_val, region_val]])
    prediction = model.predict(input_data)
    st.success(f"Estimated Annual Premium: ${prediction[0]:,.2f}")

