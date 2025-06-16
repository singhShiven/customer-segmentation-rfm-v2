# 🧠 Customer Segmentation with RFM Analysis

🚀 **Objective:** Segment e-commerce customers based on purchase behavior using RFM (Recency, Frequency, Monetary) analysis, and build an interactive dashboard using Streamlit.

---

## 📌 Problem Statement

E-commerce businesses need to target the right customers — but without data, they waste marketing budget. This project segments customers into meaningful groups to improve retention, increase revenue, and optimize campaigns.

---

## 📊 Tools Used

- Python (Pandas, Numpy)
- Scikit-learn (for clustering)
- Matplotlib / Seaborn / Plotly
- Streamlit
- Jupyter Notebook

---

## 📂 Project Structure
```
customer-segmentation-rfm-dashboard/
├── Customer_RFM_Analysis.ipynb
├── images/
│ ├── dashboard_preview.png
│ └── rfm_plot.png
├── README.md

```
---

## ⚙️ How It Works

1. **Data Cleaning & Preprocessing**  
   - Loaded raw transaction data (date, customer ID, amount).
   - Removed nulls, duplicates, and filtered valid records.

2. **RFM Feature Engineering**  
   - **Recency**: Days since last purchase  
   - **Frequency**: Total number of purchases  
   - **Monetary**: Total amount spent

3. **RFM Scoring & Segmentation**  
   - Scaled each RFM value using quantile-based scoring.
   - Assigned customer segments (e.g., Loyal, At Risk, Big Spenders).
   - 
5. **Dashboard with Streamlit**  
   - Created an interactive web app to filter segments, view charts, and export insights.

---

## 📈 Results

- Identified top 3 customer segments based on RFM scoring.
- Visualized customer behavior and trends in an interactive dashboard.
- Enabled stakeholders to take targeted marketing actions using clear, data-driven insights.

Sample Insights:
- 🟢 Loyal Customers: High frequency and monetary value — ideal for upselling.
- 🟡 At-Risk Customers: Long recency — target with win-back campaigns.
- 🔴 Low Value Customers: Low on all metrics — minimize spend.

---

## 🚀 Try It Yourself

> 👇 Click below to launch the live dashboard (hosted via Streamlit Cloud):

🔗 [Launch the App](https://share.streamlit.io/singhShiven/customer-segmentation-rfm/main/Customer_RFM_Analysis.ipynb)

> 🧑‍💻 Or run it locally:

```bash
git clone https://github.com/singhShiven/customer-segmentation-rfm.git
cd customer-segmentation-rfm
streamlit run Customer_RFM_Analysis.ipynb



