
<p align="center">
  <a href="https://github.com/singhShiven/customer-segmentation-rfm-v2/stargazers">
    <img src="https://img.shields.io/github/stars/singhShiven/customer-segmentation-rfm-v2?style=social" alt="GitHub stars">
  </a>
  <a href="https://customer-segmentation-rfm-v2-mgvq3ojoeeq3bq7j5iph9c.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/Live%20App-Streamlit-green?logo=streamlit" alt="Streamlit App">
  </a>
  <a href="https://github.com/singhShiven/customer-segmentation-rfm-v2/commits/main">
    <img src="https://img.shields.io/github/last-commit/singhShiven/customer-segmentation-rfm-v2" alt="Last Commit">
  </a>
  <a href="https://github.com/singhShiven/customer-segmentation-rfm-v2/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/singhShiven/customer-segmentation-rfm-v2" alt="License">
  </a>
</p>

# 📊 Customer Segmentation using RFM (Recency, Frequency, Monetary) Analysis

This project performs **RFM analysis** on e-commerce transaction data to segment customers into meaningful groups like `Champions`, `Loyal Customers`, `Churned Customers`, and more.

**Live App**: [Click here to try it out 🚀](https://customer-segmentation-rfm-v2-hxn5ksd9a3i7wseicj6lfy.streamlit.app/)

---

## 📁 Features

- Upload your own CSV or use default sample data
- RFM Score calculation:
  - **Recency** – Days since last purchase
  - **Frequency** – Total number of purchases
  - **Monetary** – Total amount spent
- RFM segmentation logic with label assignment (e.g., Champions, Churned)
- Interactive visualizations using Plotly:
  - Bar chart of customer count by segment
  - Average RFM values per segment
- Downloadable CSV with RFM scores
- Segment filtering using multiselect

---

## 🧪 Exploratory Data Analysis (in Notebook)

In the accompanying Jupyter notebook:
- Cleaned and preprocessed the dataset
- Verified null values and dropped rows with missing `CustomerID`
- Performed basic descriptive analysis on Quantity, UnitPrice, and InvoiceDate
- Visualized top purchasing customers and time-based purchase trends
- Implemented and validated the RFM calculation before deploying to Streamlit

---

## 📊 RFM Segmentation Logic

- Customers are scored 1–5 based on quantiles for Recency (R), Frequency (F), and Monetary (M)
- Scores are concatenated into a `RFM_Score` (e.g., `555`, `511`)
- Segments are assigned based on rules, for example:
  - `555` → Champions
  - High R & F but low M → Loyal Customers
  - Low R, F, M → Churned

---

## 🛠️ Tech Stack

- Python (Pandas, NumPy)
- Streamlit (for web app)
- Plotly Express (interactive charts)
- Jupyter Notebook (EDA and RFM logic testing)

---

## 📁 File Structure
```
customer-segmentation-rfm-v2/
│
├── Customer_RFM_Analysis.ipynb # Jupyter notebook for EDA and RFM logic
├── requirements.txt # Dependencies
├── README.md # Project readme
├── rfm/ # Contains data (data.csv)
│ └── data.csv
├── images/ # Output plots
│ ├── Average RFM Values per segment.png
│ ├── Customer Distribution by Segment.png
│ └── RFM Table Preview.png
```
## 🧪 Exploratory Data Analysis (in Notebook)

Performed in `Customer_RFM_Analysis.ipynb`:
- Cleaned and structured transactional data
- Generated **RFM metrics** using customer purchase history
- Created **visualizations** to analyze:
  - Customer distribution by segment
  - Average RFM scores
  - Preview of RFM score table

Images are saved under the `images/` folder and used in the Streamlit app.

---

## 📊 RFM Segmentation Logic

Each customer is scored on:
- **Recency**: Days since last purchase
- **Frequency**: Total number of purchases
- **Monetary**: Total amount spent

The scores are combined to assign segments like:
- 🏆 Champions
- 💰 Loyal Customers
- ⛔️ At Risk
- 📉 Lost Customers

---

## 🚀 App Features (Streamlit)

- Upload your own transaction dataset
- View interactive RFM segments
- Analyze key metrics and distributions
- Visual display of customer segments using bar plots

---

## 📦 Installation

```bash
pip install -r requirements.txt
```
Run the Streamlit app locally:
```
streamlit run app.py
```
📚 Requirements
Python 3.7+

pandas

matplotlib

seaborn

streamlit

📂 Data
Your dataset should be stored as:
```
rfm/data.csv
```
Ensure it contains at least:

Customer ID

Invoice Date

Amount


🧠 Motivation

RFM is a proven and intuitive method for customer segmentation, especially useful in marketing, e-commerce, and sales analytics.


🛠 Future Scope (Not Yet Done)

Integration of KMeans or clustering models (currently not included)
Prediction of churn using ML
Export segment data for targeted campaigns

🧑‍💻 Author

Shivendra Singh

[GitHub Repository](https://github.com/singhShiven/customer-segmentation-rfm-v2)




