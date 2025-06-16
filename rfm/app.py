import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load data
def load_data(filepath='data.csv'):
    """Loads the e-commerce data from a CSV file."""
    try:
        df = pd.read_csv(filepath, encoding='ISO-8859-1')
        return df
    except FileNotFoundError:
        st.error(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return None

# Function to perform RFM analysis
def perform_rfm_analysis(df):
    """Performs RFM analysis on the input DataFrame."""
    if df is None:
        return None

    # Drop rows with missing CustomerID
    df.dropna(subset=['CustomerID'], inplace=True)

    # Convert InvoiceDate to datetime and extract date
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['InvoiceDateOnly'] = df['InvoiceDate'].dt.date

    # Calculate Recency
    recency_df = df.groupby('CustomerID')['InvoiceDateOnly'].max().reset_index()
    recency_df['InvoiceDateOnly'] = pd.to_datetime(recency_df['InvoiceDateOnly'])
    reference_date = pd.to_datetime(df['InvoiceDateOnly'].max()) + pd.Timedelta(days=1)
    recency_df['Recency'] = (reference_date - recency_df['InvoiceDateOnly']).dt.days

    # Calculate Frequency
    frequency_df = df.groupby('CustomerID')['InvoiceNo'].nunique().reset_index()
    frequency_df.rename(columns={'InvoiceNo': 'Frequency'}, inplace=True)

    # Calculate Monetary
    df['Total Sales'] = df['Quantity'] * df['UnitPrice']
    monetary_df = df.groupby('CustomerID')['Total Sales'].sum().reset_index()
    monetary_df.rename(columns={'Total Sales': 'Monetary'}, inplace=True)

    # Merge RFM DataFrames
    rfm_df = recency_df.merge(frequency_df, on='CustomerID').merge(monetary_df, on='CustomerID')

    # Assign RFM scores
    rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'], 5, labels=[1, 2, 3, 4, 5])

    # Create RFM Score and Segments
    rfm_df['RFM_Score'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)

    def rfm_segment(row):
        if row['RFM_Score'] == '555':
            return 'Champions'
        elif row['RFM_Score'][0] == '5' and row['RFM_Score'][1] in ['4','5'] and row['RFM_Score'][2] in ['4','5']:
            return 'Loyal Customers'
        elif row['RFM_Score'][0] == '5' and row['RFM_Score'][1] in ['1','2']:
            return 'New Customers'
        elif row['RFM_Score'][0] in ['3','4'] and row['RFM_Score'][2] in ['4','5']:
            return 'Potential Loyalists'
        elif row['RFM_Score'][0] in ['1','2']:
            return 'Churned Customers'
        else:
            return 'Others'

    rfm_df['Segment'] = rfm_df.apply(rfm_segment, axis=1)

    return rfm_df

# Main part of the Streamlit app
st.title('RFM Analysis of E-commerce Data')

st.markdown("""
This application performs an RFM (Recency, Frequency, Monetary) analysis on e-commerce sales data.
RFM is a marketing technique used to quantitatively rank and group customers based on their transaction history.
For investors, understanding customer segments through RFM can provide insights into customer value,
loyalty, and potential for future revenue, helping to inform marketing strategies and resource allocation.
""")

# Load data
data = load_data()

# Perform RFM analysis
if data is not None:
    rfm_result_df = perform_rfm_analysis(data.copy()) # Use a copy to avoid modifying the original loaded data

    if rfm_result_df is not None:
        st.subheader('RFM Table Preview')
        st.markdown("""
        This table shows a preview of the RFM analysis results for each customer.
        - **CustomerID**: Unique identifier for each customer.
        - **InvoiceDateOnly**: The date of the customer's most recent purchase.
        - **Recency**: The number of days since the customer's last purchase. Lower recency indicates a more recent purchase.
        - **Frequency**: The total number of unique purchases made by the customer. Higher frequency indicates more repeat business.
        - **Monetary**: The total amount of money spent by the customer. Higher monetary value indicates a higher-spending customer.
        - **R_Score, F_Score, M_Score**: Scores (1-5) assigned to Recency, Frequency, and Monetary based on quantiles. Higher scores generally indicate better performance (except for Recency where lower days get a higher score).
        - **RFM_Score**: A combined score string derived from the R, F, and M scores.
        - **Segment**: The customer segment assigned based on the RFM score.
        """)
        st.dataframe(rfm_result_df.head())

        st.subheader('Customer Distribution Across RFM Segments')
        st.markdown("""
        This bar chart illustrates the number of customers falling into each defined RFM segment.
        Investors can use this visualization to quickly grasp the size of different customer groups,
        such as 'Champions' (most valuable customers) or 'Churned Customers' (least recently active).
        This helps in understanding the current customer base composition and identifying segments that might require specific attention (e.g., re-engagement campaigns for churned customers).
        """)
        plt.figure(figsize=(10, 6))
        sns.countplot(x='Segment', data=rfm_result_df, order=rfm_result_df['Segment'].value_counts().index)
        plt.title('Number of Customers per RFM Segment')
        plt.xlabel('RFM Segment')
        plt.ylabel('Number of Customers')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(plt)

        segment_characteristics = rfm_result_df.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean()

        segment_characteristics_melted = segment_characteristics.reset_index().melt(id_vars='Segment', var_name='Metric', value_name='Average Value')

        st.subheader('Average RFM Values per Segment')
        st.markdown("""
        This bar chart displays the average Recency, Frequency, and Monetary values for each customer segment.
        For investors, this visualization helps in understanding the typical behavior and value of customers within each segment.
        For example, 'Champions' have low average recency (recent purchases), high average frequency (frequent purchases), and high average monetary values (high spending), confirming their high value.
        'Churned Customers', on the other hand, show high average recency (not purchased recently), low average frequency, and low average monetary values, indicating their lower engagement and value.
        This information is crucial for tailoring marketing campaigns and resource allocation to maximize ROI for each segment.
        """)
        plt.figure(figsize=(12, 7))
        sns.barplot(x='Segment', y='Average Value', hue='Metric', data=segment_characteristics_melted, palette='viridis')
        plt.title('Average RFM Values per Segment')
        plt.xlabel('RFM Segment')
        plt.ylabel('Average Value')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='RFM Metric')
        plt.tight_layout()
        st.pyplot(plt)


