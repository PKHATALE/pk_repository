import streamlit as st
import random

# --- Prediction Logic (Simulated Model) ---

def predict_charge(data):
   
    try:
        # Get inputs
        age = data.get('age')
        bmi = data.get('bmi')
        children = data.get('children')
        sex = data.get('sex')
        smoker = data.get('smoker')
        region = data.get('region')
        
        # Base annual cost (intercept)
        base_charge = 8000.0

        # Age effect: linear increase, steepens slightly after 40
        age_factor = age * 250.0 
        if age > 40:
            age_factor += (age - 40) * 150.0

        # BMI effect: Linear increase, non-linear increase (penalty) for high BMI (>30)
        bmi_factor = bmi * 120.0
        if bmi > 30:
            bmi_factor += (bmi - 30) * 500.0 # High BMI penalty

        # Smoker effect: massive penalty
        smoker_factor = 0
        if smoker == 'yes':
            smoker_factor = 25000.0 # Smoking is the largest cost driver

        # Children effect: minor cost per dependent
        children_factor = children * 400.0

        # Sex effect: minor difference
        sex_factor = 0
        if sex == 'male':
            sex_factor = 150.0
            
        # Region effect: Southeast typically has higher costs
        region_factor = 0
        if region == 'southeast':
            region_factor = 1200.0
        elif region == 'northeast':
            region_factor = 500.0
        # Southwest and Northwest are used as baseline (0 or near 0)
        
        # Calculate final charge
        charge = (base_charge + age_factor + bmi_factor + smoker_factor + 
                  children_factor + sex_factor + region_factor)
        
        # Apply a small amount of random noise for realism
        noise = random.uniform(-500, 500)
        final_charge = max(100, charge + noise) # Ensure charge is at least 100

        # Return the result rounded to two decimal places
        return round(final_charge, 2)

    except Exception as e:
        # Streamlit handles errors gracefully
        st.error(f"Error during calculation: {e}")
        return None

# --- Streamlit UI ---

def main():
    # Set page configuration for a modern look
    st.set_page_config(page_title="Insurance Premium Predictor", layout="centered")

    # Custom CSS for styling (mimics the original app's gradient style)
    st.markdown("""
        <style>
        .title-gradient {
            background: -webkit-linear-gradient(45deg, #1e3a8a, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .stButton>button {
            background-color: #3b82f6;
            color: white;
            font-weight: 600;
            padding: 0.75rem 1rem;
            border-radius: 0.75rem;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #2563eb;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.5);
        }
        .result-box {
            background-color: #e5f5e5;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #34d399;
        }
        .result-charge {
            font-size: 3rem;
            font-weight: 800;
            color: #10b981; /* green-500 */
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title and description
    st.markdown('<p class="title-gradient">  Health Insurance Premium Predictor</p>', unsafe_allow_html=True)
    #st.markdown('<p style="text-align: center; color: #555;">Estimate your annual health insurance premium charge.</p>', unsafe_allow_html=True)
    
    st.markdown("---")

    # --- Input Fields using st.form for a single submission button ---
    
    with st.form("insurance_form"):
        st.subheader("Personal Information")

        # Age and BMI in columns
        col1, col2 = st.columns(2)
        with col1:
            # Slider for age for easy selection
            age = st.slider("Age", min_value=18, max_value=64, value=30, step=1)
        with col2:
            # Number input for BMI
            bmi = st.number_input("BMI (Body Mass Index)", min_value=15.0, max_value=55.0, value=25.0, step=0.1)

        # Children and Sex in columns
        col3, col4 = st.columns(2)
        with col3:
            children = st.number_input("Number of Children", min_value=0, max_value=5, value=0, step=1)
        with col4:
            # Radio for Sex
            sex = st.radio("Sex", ("female", "male"), horizontal=True)

        st.subheader("Lifestyle and Location")
        
        # Smoker and Region in columns
        col5, col6 = st.columns(2)
        with col5:
            # Radio for Smoker status
            smoker = st.radio("Smoker Status", ("no", "yes"), horizontal=True)
        with col6:
            # Selectbox for Region
            region = st.selectbox("Region", ("southeast", "southwest", "northeast", "northwest"))

        # Form submission button
        submitted = st.form_submit_button("Predict Premium")

    # --- Prediction & Result Display ---
    if submitted:
        # Collect data into the required dictionary format for the predict function
        input_data = {
            'age': age,
            'bmi': bmi,
            'children': children,
            'sex': sex,
            'smoker': smoker,
            'region': region
        }
        
        # Calculate prediction with a loading spinner
        with st.spinner('Calculating premium...'):
            charge = predict_charge(input_data)
        
        if charge is not None:
            formatted_charge = f"${charge:,.2f}"
            
            # Display result in a styled box
            st.markdown(
                f"""
                <div class="result-box">
                    <p style="font-size: 1.2rem; color: #333; margin-bottom: 0;">Estimated Annual Charge:</p>
                    <p class="result-charge">{formatted_charge}</p>
                    <p style="font-size: 0.75rem; color: #777; margin-top: 10px;">*This is an estimate based on a simulated model.</p>
                </div>
                """, unsafe_allow_html=True
            )


if __name__ == '__main__':
    main()




