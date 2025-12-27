import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. Page Config & Custom Styling
st.set_page_config(page_title="Price Optimizer", layout="wide")
st.title("Price Optimization Dashboard")
st.markdown("""*Bree Thomas Portfoilo: This tool analyzes price sensitivity and simulates revenue 
impacts based on historical markdown data.*""")

# 2. Sidebar - Data Upload & Links
with st.sidebar:
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Upload your CSV", type="csv")
    
    st.markdown("---")
    st.subheader("Try Sample Data")
    st.caption("Download and re-upload these to see different behaviors:")
    st.markdown("[High-End Tech (Inelastic)](https://raw.githubusercontent.com/yadav-shobhit/Price-Elasticity/master/data.csv)")
    st.markdown("[Generic Superstore (Elastic)](https://raw.githubusercontent.com/tushar2704/Superstore-Sales-Dashboard-with-Streamlit/main/Sample%20-%20Superstore.csv)")

# 3. Core Logic
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Simple Data Cleaning for your specific dataset
    df['is_returned'] = df['is_returned'].fillna(False)
    
    # --- BUSINESS QUESTIONS SECTION ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Profit vs. Returns Analysis")
        # Visualizing if higher markdowns lead to more returns (The 'Human' touch)
        fig_return = px.box(df, x='markdown_percentage', y='is_returned', 
                            title="Do Markdowns Drive Returns?",
                            color_backend='brand')
        st.plotly_chart(fig_return)

    with col2:
        st.subheader("Price Elasticity Simulator")
        # Creating a simple slider for 'What-If' scenarios
        price_adj = st.slider("Adjust Price Change (%)", -50, 50, 0)
        
        # Logic: If we lower price by X, demand increases by Y
        # We assume a base elasticity of -1.5 for fashion (changeable)
        elasticity = -1.5 
        new_demand_change = (price_adj * elasticity) / 100
        st.metric("Predicted Volume Change", f"{new_demand_change*100:.1f}%")

    # --- THE "SO WHAT?" RECOMMENDATION ---
    st.info("💡 **BA Recommendation:** Based on current return rates and markdown sensitivity, "
            "avoid markdowns over 30% for 'Outerwear' as it triggers quality-related returns.")

else:
    st.warning("Please upload a CSV file to begin the analysis.")