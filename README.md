<<<<<<< HEAD
# RFM-customer-segmentation
Customer segmentation project using RFM (Recency, Frequency, Monetary) analysis to identify customer value, loyalty, and churn risk. Built with Python, Excel, and Power BI using the Online Retail II dataset.
=======
# Customer Segmentation Using RFM Analysis

## Business Question

Which customers are most valuable, which are at risk of churning, and where should a retention budget be focused?

## Tools Used

- Python
- Pandas
- Matplotlib
- Excel
- Power BI

## Dataset

This project uses the **Online Retail II** dataset containing **1,067,371 transaction records**.

The dataset contains information about:

- Invoice numbers
- Products
- Quantities
- Transaction dates
- Prices
- Customer IDs
- Countries

Dataset file:

`online_retail_II.csv`

## Project Overview

This project uses **RFM (Recency, Frequency, Monetary) analysis** to segment customers based on their purchasing behavior.

The analysis includes:

- Data cleaning
- Customer-level RFM calculation
- RFM scoring
- Customer segmentation
- Segment-level revenue analysis
- Data visualization
- Excel-based customer analysis
- Interactive Power BI dashboard

## Data Cleaning

The dataset was cleaned by:

- Removing transactions without a Customer ID
- Removing cancelled transactions with negative quantities
- Converting transaction dates into datetime format
- Calculating transaction-level revenue using Quantity × Price

After cleaning:

- **805,620 transactions**
- **5,881 unique customers**

## RFM Analysis

### Recency

Number of days since a customer's most recent purchase.

Lower recency indicates a more recent customer.

### Frequency

Number of distinct orders placed by a customer.

Higher frequency indicates more frequent purchasing.

### Monetary

Total amount spent by a customer.

Higher monetary value indicates higher customer spending.

Each RFM metric was divided into quartiles and scored from **1 to 4**. The scores were then combined to create customer segments.

## Customer Segments

The analysis identifies six customer segments:

- Champions
- Loyal Customers
- At Risk
- Needs Attention
- Lost
- New / Recent

## Segment Results

| Segment | Customers | % of Customers | Revenue | % of Revenue |
|---|---:|---:|---:|---:|
| Champions | 1,814 | 30.8% | $13,463,546.60 | 75.9% |
| At Risk | 650 | 11.1% | $2,128,358.10 | 12.0% |
| Loyal Customers | 803 | 13.7% | $791,828.90 | 4.5% |
| Needs Attention | 501 | 8.5% | $652,863.20 | 3.7% |
| Lost | 1,776 | 30.2% | $575,787.10 | 3.2% |
| New / Recent | 337 | 5.7% | $131,045.20 | 0.7% |

## Key Findings

- **Champions** represent 30.8% of customers but account for **75.9% of historical revenue**.
- **At Risk** customers represent 11.1% of customers and account for **12.0% of historical revenue**.
- **Lost** customers represent 30.2% of customers but account for only 3.2% of historical revenue.
- The results show that customer count and revenue contribution are distributed very differently across customer segments.

## Visualizations

The project includes:

- Customer count by segment
- Frequency vs. Monetary value by customer segment

## Power BI Dashboard

The Power BI dashboard includes:

- Customer count by segment
- Total customer revenue
- Revenue by customer segment
- Average customer recency
- Frequency vs. Monetary value analysis
- Segment filter
- RFM Score filter

Power BI file:

`Customer_Segmentation_RFM.pbix`

## Project Files

- `online_retail_II.csv` — Online Retail II transaction dataset
- `analysis.py` — Python RFM analysis and visualization script
- `RFM_Customer_Segmentation.xlsx` — Customer-level RFM analysis
- `Customer_Segmentation_RFM.pbix` — Interactive Power BI dashboard
- `chart_segment_counts.png` — Customer count by segment
- `chart_frequency_vs_monetary.png` — Frequency vs. Monetary visualization
- `README.md` — Project documentation

## How to Run

Install the required Python libraries:

```bash
pip install pandas matplotlib

Run the analysis:

python analysis.py

- The script performs data cleaning, calculates RFM metrics, assigns customer segments, generates the segment summary, and creates visualizations.

Open Customer_Segmentation_RFM.pbix to view the interactive Power BI dashboard.

Skills Demonstrated
Python
Pandas
Matplotlib
Excel
Power BI
RFM Analysis
Data Cleaning
Customer Segmentation
Exploratory Data Analysis
Data Visualization
Dashboard Development
Business Insights
>>>>>>> 5880825 (Upload RFM project files)
