import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Retail Price Optimizer", layout="wide")

# --- 1. Data Loading Logic ---
@st.cache_data
def load_data(file_source):
    if file_source == "Default: Fashion Boutique":
        return pd.read_csv("fashion_boutique_dataset.csv")
    elif file_source == "Tech Sales (Placeholder)":
        return pd.DataFrame({"item": ["Laptop"], "current_price": [1000], "markdown_percentage": [0], "is_returned": [False]})
    elif file_source == "Grocery Data (Placeholder)":
        return pd.DataFrame({"item": ["Apple"], "current_price": [1], "markdown_percentage": [0], "is_returned": [False]})
    else:
        return pd.read_csv(file_source)

# --- 2. Sidebar Selection ---
with st.sidebar:
    st.markdown("**DATA SELECTION**")
    data_option = st.selectbox(
        "Choose Dataset to Analyze",
        ["Default: Fashion Boutique", "Tech Sales (Placeholder)", "Grocery Data (Placeholder)"]
    )
    st.info(f"Using: {data_option}")
    
    st.markdown("---")
    st.markdown("**UPLOAD CUSTOM DATA**")
    uploaded_file = st.file_uploader("Drag and drop additional files here", type="csv")

# Data loading
df = load_data(uploaded_file if uploaded_file else data_option)

# Data Cleaning
if 'is_returned' in df.columns:
    df['is_returned'] = df['is_returned'].fillna(False)

# --- 3. Main Body Content ---
st.markdown("# REVENUE AND PRICE OPTIMIZATION STRATEGY")
st.markdown("---")

st.markdown("""
**DASHBOARD GUIDE**
* **Price Sensitivity:** Calculates how customer demand shifts when prices change.
* **Revenue Simulation:** Predicts total sales impact based on price adjustments.
* **Return Analysis:** Monitors if heavy discounting increases product return rates.
* **Optimization:** Identifies the 'Sweet Spot'—the price point that maximizes total revenue.
""")

# Key Metrics
if 'current_price' in df.columns:
    total_revenue = df['current_price'].sum()
    m1, m2 = st.columns(2)
    m1.metric("Current Total Revenue", f"${total_revenue:,.2f}")
    m2.metric("Data Records Analyzed", f"{len(df):,}")

# --- 4. Simulation & Dynamic Summary ---
st.markdown("---")
st.markdown("### **PRICE ELASTICITY SIMULATOR**")

col_sim1, col_sim2 = st.columns([1, 2])

with col_sim1:
    st.markdown("**SIMULATION CONTROLS**")
    st.write("""
    Adjust the slider to simulate a store-wide price change. 
    Increasing prices (right) may lower volume but increase margin per unit. 
    Decreasing prices (left) simulates a sale to drive volume.
    """)
    
    price_change = st.slider("Target Price Adjustment (%)", -50, 50, 0)
    
    # Elasticity Logic
    elasticity = -1.6
    demand_impact = (price_change * elasticity) / 100
    new_revenue = total_revenue * (1 + (price_change/100)) * (1 + demand_impact)
    revenue_delta = new_revenue - total_revenue
    
    # Simple Return Insight Logic
    # If the price is dropped significantly, warn about the "Discount-Return Trap"
    return_risk = "LOW"
    risk_msg = "Stable return patterns expected."
    if price_change < -25:
        return_risk = "HIGH"
        risk_msg = "Deep discounts historically lead to higher return rates due to 'impulse' buying."

with col_sim2:
    # THE DYNAMIC SUMMARY
    diff_symbol = "+" if revenue_delta >= 0 else ""
    st.markdown(f"""
    **EXECUTIVE IMPACT SUMMARY**
    * **Target Price Change:** `{price_change}%`
    * **Predicted Volume Shift:** `{ (demand_impact * 100):.1f}%`
    * **New Projected Total:** `${new_revenue:,.2f} ({diff_symbol}${revenue_delta:,.2f})`
    * **Return Risk Level:** `{return_risk}` ({risk_msg})
    """)
    st.markdown("---")

    # Revenue Curve Visualization
    sim_prices = np.linspace(-0.5, 0.5, 20)
    sim_revs = [total_revenue * (1 + p) * (1 + (p * elasticity)) for p in sim_prices]
    fig_curve = px.line(x=sim_prices*100, y=sim_revs, 
                        labels={'x': 'Price Change %', 'y': 'Revenue ($)'}, 
                        title="REVENUE OPTIMIZATION CURVE")
    fig_curve.add_vline(x=price_change, line_dash="dash", line_color="red")
    st.plotly_chart(fig_curve, use_container_width=True)

# --- 5. Returns ---
st.markdown("---")
st.markdown("### **RETURN LOGISTICS ANALYSIS**")
if 'is_returned' in df.columns:
    fig_box = px.box(df, x='category', y='markdown_percentage', color='is_returned',
                     title="Markdown Spread vs. Returns")
    st.plotly_chart(fig_box, use_container_width=True)
