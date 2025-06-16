import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="RFM Analysis", layout="wide")
st.title('RFM Analysis of E-commerce Data')

@st.cache_data
def load_data(uploaded_file):
    """Loads the e-commerce data from an uploaded file or defaults to 'data.csv'."""
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
            st.success("Data loaded successfully from uploaded file!")
            return df
        except Exception as e:
            st.error(f"Error loading uploaded file: {e}")
            st.info("Attempting to load default data.csv...")
            return load_data_default()
    else:
        st.info("Upload a CSV file or the default data.csv will be used.")
        return load_data_default()

@st.cache_data
def load_data_default(filepath='rfm/data.csv'):
    """Loads the e-commerce data from the default 'data.csv' file."""
    try:
        df = pd.read_csv(filepath, encoding='ISO-8859-1')
        st.success("Data loaded successfully from default data.csv!")
        return df
    except FileNotFoundError:
        st.error(f"Error: Default file not found at {filepath}")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the default data: {e}")
        return None

uploaded_file = st.file_uploader("Upload your CSV data file", type=["csv"])
data = load_data(uploaded_file)

if data is not None:
    st.write("Data Preview:")
    st.dataframe(data.head())

def perform_rfm_analysis(df):
    """Performs RFM analysis on the input DataFrame."""
    if df is None:
        return None

    required_cols = ['CustomerID', 'InvoiceDate', 'InvoiceNo', 'Quantity', 'UnitPrice']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"The following required columns are missing: {', '.join(missing_cols)}")
        return None

    df.dropna(subset=['CustomerID'], inplace=True)

    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['InvoiceDateOnly'] = df['InvoiceDate'].dt.date

    # Recency
    recency_df = df.groupby('CustomerID')['InvoiceDateOnly'].max().reset_index()
    recency_df['InvoiceDateOnly'] = pd.to_datetime(recency_df['InvoiceDateOnly'])
    reference_date = pd.to_datetime(df['InvoiceDateOnly'].max()) + pd.Timedelta(days=1)
    recency_df['Recency'] = (reference_date - recency_df['InvoiceDateOnly']).dt.days

    # Frequency
    frequency_df = df.groupby('CustomerID')['InvoiceNo'].nunique().reset_index()
    frequency_df.rename(columns={'InvoiceNo': 'Frequency'}, inplace=True)

    # Monetary
    df['Total Sales'] = df['Quantity'] * df['UnitPrice']
    monetary_df = df.groupby('CustomerID')['Total Sales'].sum().reset_index()
    monetary_df.rename(columns={'Total Sales': 'Monetary'}, inplace=True)

    # Merge
    rfm_df = recency_df.merge(frequency_df, on='CustomerID').merge(monetary_df, on='CustomerID')

    rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'], 5, labels=[1, 2, 3, 4, 5])
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

if data is not None:
    rfm_result_df = perform_rfm_analysis(data.copy())

    if rfm_result_df is not None:
        st.subheader('RFM Table Preview')
        st.markdown("""
        - **CustomerID**: Unique identifier
        - **Recency**: Days since last purchase
        - **Frequency**: Total transactions
        - **Monetary**: Total amount spent
        - **RFM Score**: Combination of R, F, M
        - **Segment**: Categorized customer group
        """)
        st.dataframe(rfm_result_df.head())

if data is not None and rfm_result_df is not None:
    st.subheader('Customer Distribution Across RFM Segments')
    segment_counts = rfm_result_df['Segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Number of Customers']

    fig_segment_counts = px.bar(
        segment_counts,
        x='Segment',
        y='Number of Customers',
        title='Number of Customers per RFM Segment',
        labels={'Segment': 'RFM Segment', 'Number of Customers': 'Number of Customers'},
        color='Segment'
    )
    st.plotly_chart(fig_segment_counts, use_container_width=True)

if data is not None and rfm_result_df is not None:
    st.subheader('Average RFM Values per Segment')
    segment_characteristics = rfm_result_df.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean()
    segment_characteristics_melted = segment_characteristics.reset_index().melt(id_vars='Segment', var_name='Metric', value_name='Average Value')

    fig_segment_values = px.bar(
        segment_characteristics_melted,
        x='Segment',
        y='Average Value',
        color='Metric',
        barmode='group',
        title='Average RFM Values per Segment',
        labels={'Segment': 'RFM Segment', 'Average Value': 'Average Value', 'Metric': 'RFM Metric'},
        color_discrete_map={'Recency': 'lightblue', 'Frequency': 'salmon', 'Monetary': 'lightgreen'}
    )
    st.plotly_chart(fig_segment_values, use_container_width=True)

if data is not None and rfm_result_df is not None:
    st.subheader('Summary Insights')
    st.markdown("""
    - **Champions**: Recent, frequent, high-spending
    - **Loyal Customers**: Frequent buyers
    - **New Customers**: Recent but not frequent
    - **Potential Loyalists**: On path to loyalty
    - **Churned Customers**: Inactive or disengaged
    """)

    st.subheader('Download RFM Results')
    csv_data = rfm_result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download RFM Results as CSV",
        data=csv_data,
        file_name='rfm_results.csv',
        mime='text/csv',
    )

if data is not None and rfm_result_df is not None:
    st.subheader('Filter by Segment')
    all_segments = rfm_result_df['Segment'].unique().tolist()
    selected_segments = st.multiselect(
        'Select one or more segments to display:',
        all_segments,
        default=all_segments
    )
    if selected_segments:
        filtered_rfm_df = rfm_result_df[rfm_result_df['Segment'].isin(selected_segments)]
        st.write('Filtered RFM Data:')
        st.dataframe(filtered_rfm_df)
    else:
        st.warning("Please select at least one segment to display filtered data.")

st.markdown("""
### How to Run This Application

1. Save this code in a `.py` file (e.g., `rfm_app.py`)
2. Open terminal and run:

```bash
streamlit run rfm_app.py
""")
