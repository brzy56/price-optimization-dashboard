# Retail Price Optimizer

**[View Live Application](https://price-optimization-dashboard-ddsnuxqbzwdtwgpsy4ehjl.streamlit.app/)**

This is a retail price optimization tool. It is designed to help category managers and business owners stop guessing about pricing. It uses historical data to predict exactly how changing a price will affect sales volume and total revenue.

### What it does
* **Identifies the Optimal Price Point:** It finds the exact moment where a price increase starts to lose more money than it makes.
* **Predicts Customer Behavior:** It calculates price sensitivity to show how much sales volume you will gain or lose for every dollar you shift.
* **Protects Profit:** It monitors return rates to ensure that deep discounts are not driving impulse buys that end up being returned later.



### How to use it
1. **Select Data:** Choose a built-in retail dataset from the sidebar or upload your own.
2. **Simulate Pricing:** Use the slider to test a price change such as a 10% increase or 15% decrease.
3. **Check the Summary:** Read the One Sentence Summary to see the projected revenue and volume shift.
4. **Optimize:** Click the Run Revenue Optimization button to instantly jump to the mathematically ideal price.
5. **Audit Returns:** Review the Return Logistics section at the bottom to see which products are most sensitive to discounts.

### Data Requirements
If you upload your own data, the file must be a **.csv** with these exact column names:
* `current_price`: The original price of the item.
* `category`: The product group such as Shoes or Electronics.
* `is_returned`: Whether the item was sent back (True or False).
* `markdown_percentage`: The discount applied from 0 to 100.



### Challenges I solved
The biggest technical hurdle was making the Optimization button work with the manual slider. Streamlit typically locks a slider when you move it, which prevents a button from changing its value. I solved this by moving the slider value into a Session State background variable. This allows the user to slide manually and also allows the Optimize button to take over and move the slider automatically to the peak revenue point without the app crashing.

### Tech Used
* **Python** for the math and data logic.
* **Streamlit** for the interactive dashboard.
* **Plotly** for the revenue curves and return analysis charts.
* **Pandas and NumPy** for data processing.



---
**Bree Thomas** | Data Business Analyst | 2025
