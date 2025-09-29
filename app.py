import streamlit as st
import pickle

st.title('Health Insurance Premium Prediction')

age=st.number_input('Age:')
bmi=st.number_input('BMI:')
children=st.number_input('Children:')
gender=st.text_input('Gender:')
smoker=st.text_input('Smoker:')

model=pickle.load(open('InsuranceCharge.pkl','rb'))

if st.button('Predict'):
    gender = 0 if gender.upper()=='MALE' else 1
    smoker = 0 if smoker.upper()=='NO' else 1
    X_test = [[age,bmi,children,gender,smoker]]
    yp= str(round(model.predict(X_test)[0],2))
    st.write('Your Premium is:'+yp)
