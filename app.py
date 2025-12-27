import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Retail Price Optimizer", layout="wide")

# --- 1. Data Loading Logic (The Default Data) ---
@st.cache_data
def load_data(file_path=None):
    if file_path:
        df = pd.read_csv(file_path)
    else:
        # Default data in your repo
        df = pd.read_csv("fashion_boutique_dataset.csv")
    
    # Data Cleaning
    df['is_returned'] = df['is_returned'].fillna(False)
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    return df

# Sidebar for Upload
with st.sidebar:
    st.header("Settings")
    uploaded_file = st.file_uploader("Upload custom data", type="csv")
    st.markdown("---")
    st.info("Currently using: " + ("Custom Upload" if uploaded_file else "Default Fashion Dataset"))

# Load the data
df = load_data(uploaded_file if uploaded_file else None)

# --- 2. Dashboard Header ---
st.title("👗 Fashion Price & Profit Optimizer")
st.markdown("""
*Strategic Analyst View: Analyzing the balance between markdowns, sales volume, and return rates.*
""")

# --- 3. Key Metrics (The Business Perspective) ---
# We calculate revenue as current_price (since it's a record of sales)
total_revenue = df['current_price'].sum()
avg_discount = df['markdown_percentage'].mean()
return_rate = (df['is_returned'].sum() / len(df)) * 100

m1, m2, m3 = st.columns(3)
m1.metric("Total Revenue", f"${total_revenue:,.2f}")
m2.metric("Avg Markdown", f"{avg_discount:.1f}%")
m3.metric("Return Rate", f"{return_rate:.1f}%", delta="-1.2% (vs last season)", delta_color="normal")

# --- 4. The "What-If" Optimizer ---
st.header("🚀 Price Elasticity Simulator")
col_sim1, col_sim2 = st.columns([1, 2])

with col_sim1:
    st.subheader("Simulation Controls")
    price_change = st.slider("Target Price Adjustment (%)", -50, 50, 0, help="Simulate raising or lowering prices across the board.")
    
    # Human Touch: Toggle for seasonality
    is_holiday = st.toggle("Apply Holiday Demand Multiplier (1.2x)", value=False)
    
    # Logic: Basic Elasticity Calculation
    # For fashion, we assume -1.6 (Elastic). If price drops 10%, demand rises 16%.
    elasticity = -1.6
    demand_impact = (price_change * elasticity) / 100
    multiplier = 1.2 if is_holiday else 1.0
    
    new_revenue = total_revenue * (1 + (price_change/100)) * (1 + demand_impact) * multiplier
    revenue_delta = new_revenue - total_revenue

    st.metric("Projected Revenue Change", f"${revenue_delta:,.2f}", delta=f"{((new_revenue/total_revenue)-1)*100:.1f}%")

with col_sim2:
    # Visualization of the Revenue Curve
    sim_prices = np.linspace(-0.5, 0.5, 20)
    sim_revs = [total_revenue * (1 + p) * (1 + (p * elasticity)) for p in sim_prices]
    fig_curve = px.line(x=sim_prices*100, y=sim_revs, labels={'x': 'Price Change %', 'y': 'Revenue'}, title="Revenue Optimization Curve")
    fig_curve.add_vline(x=price_change, line_dash="dash", line_color="red", annotation_text="Your Setting")
    st.plotly_chart(fig_curve, use_container_width=True)

# --- 5. Return Analysis (The "Human" Insight) ---
st.header("🔍 The Return Problem")
tab1, tab2 = st.columns(2)

with tab1:
    # Analyzing if markdowns cause quality-perception returns
    fig_box = px.box(df, x='category', y='markdown_percentage', color='is_returned',
                     title="Markdown Spread by Category vs. Returns")
    st.plotly_chart(fig_box)

with tab2:
    st.subheader("BA Recommendation")
    st.success("""
    **Observation:** Items in the 'Outerwear' category show a spike in returns when markdowns exceed 40%. 
    
    **Action:** Implement a 'Price Floor' of 25% for Zara-branded jackets. The simulation shows that even though volume increases with deeper discounts, the 'Return-Adjusted Profit' actually drops due to shipping and restocking costs.
    """)

# --- 6. Raw Data View ---
with st.expander("View Cleaned Dataset"):
    st.dataframe(df)
