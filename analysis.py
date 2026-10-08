"""
Customer Segmentation using RFM Analysis
------------------------------------------
Project: Segment an e-commerce customer base by Recency, Frequency, and
Monetary value to identify high-value customers and customers at risk of
churning - using plain business logic, no black-box ML model.

Run this file top to bottom. Every step below is something you should be
able to explain in an interview: WHAT it does, HOW, and WHY it matters.
"""

import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)

# ============================================================
# STEP 1: LOAD THE DATA
# ============================================================
df = pd.read_csv("online_retail_II.csv")

print("=== STEP 1: Raw data overview ===")
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
print(df.head(3))
print()

# ============================================================
# STEP 2: CLEAN THE DATA
# ============================================================
# WHY: RFM analysis is built entirely on per-customer transaction totals,
# so bad rows (missing customer ID, cancelled orders) would corrupt every
# customer's score if left in.

print("=== STEP 2: Cleaning ===")

before = len(df)

# 2a. Drop rows with no Customer ID (guest checkouts) - can't segment a
#     customer we can't identify
df = df.dropna(subset=["Customer ID"])

# 2b. Remove cancelled/returned orders (negative quantity) - these aren't
#     real purchases and would understate a customer's true spend
df = df[df["Quantity"] > 0]

after = len(df)
print(f"Removed {before - after} rows (missing customer ID or cancelled orders)")

# 2c. Convert date and add a computed revenue column
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["LineTotal"] = df["Quantity"] * df["Price"]

print(f"Remaining rows: {len(df)}, unique customers: {df['Customer ID'].nunique()}")
print()

# ============================================================
# STEP 3: CALCULATE RFM METRICS PER CUSTOMER
# ============================================================
# WHAT: For every customer, calculate:
#   Recency   = days since their most recent purchase
#   Frequency = number of distinct orders they've placed
#   Monetary  = total amount they've spent
# WHY: These three numbers together describe customer VALUE and ENGAGEMENT
# far better than any single metric alone - a customer who spent a lot once
# a year ago is a very different business problem than one who buys weekly.

print("=== STEP 3: RFM Calculation ===")

snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("Customer ID").agg(
    Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
    Frequency=("Invoice", "nunique"),
    Monetary=("LineTotal", "sum"),
).reset_index()

rfm["Monetary"] = rfm["Monetary"].round(2)

print(rfm.describe().round(1))
print()

# ============================================================
# STEP 4: SCORE AND SEGMENT CUSTOMERS
# ============================================================
# WHAT: Split each metric into quartiles (1-4) and combine into a segment.
# HOW: pd.qcut divides customers into 4 equal-sized buckets per metric.
#      Recency is scored in REVERSE (lower days = better = higher score).
# WHY: This turns three raw numbers into a simple, explainable label a
# marketing team can act on immediately - no ML model, no black box.

print("=== STEP 4: Scoring ===")

rfm["R_score"] = pd.qcut(rfm["Recency"], 4, labels=[4, 3, 2, 1]).astype(int)
rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
rfm["M_score"] = pd.qcut(rfm["Monetary"], 4, labels=[1, 2, 3, 4]).astype(int)

rfm["RFM_Score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]


def segment_customer(row):
    if row["R_score"] >= 3 and row["F_score"] >= 3 and row["M_score"] >= 3:
        return "Champions"
    elif row["R_score"] >= 3 and row["F_score"] >= 2:
        return "Loyal Customers"
    elif row["R_score"] <= 2 and row["F_score"] >= 3 and row["M_score"] >= 3:
        return "At Risk"
    elif row["R_score"] >= 3 and row["F_score"] <= 2:
        return "New / Recent"
    elif row["R_score"] <= 2 and row["F_score"] <= 2 and row["M_score"] <= 2:
        return "Lost"
    else:
        return "Needs Attention"


rfm["Segment"] = rfm.apply(segment_customer, axis=1)

print(rfm[["Customer ID", "Recency", "Frequency", "Monetary", "RFM_Score", "Segment"]].head(10))
print()

# ============================================================
# STEP 5: SEGMENT SUMMARY (the business-facing output)
# ============================================================
print("=== STEP 5: Segment Summary ===")

segment_summary = rfm.groupby("Segment").agg(
    num_customers=("Customer ID", "count"),
    avg_recency_days=("Recency", "mean"),
    avg_frequency=("Frequency", "mean"),
    total_monetary=("Monetary", "sum"),
    avg_monetary=("Monetary", "mean"),
).round(1).sort_values("total_monetary", ascending=False)

segment_summary["pct_of_customers"] = (
    segment_summary["num_customers"] / segment_summary["num_customers"].sum() * 100
).round(1)
segment_summary["pct_of_revenue"] = (
    segment_summary["total_monetary"] / segment_summary["total_monetary"].sum() * 100
).round(1)

print(segment_summary)
print()

rfm.to_csv("rfm_customer_segments.csv", index=False)
print("Saved full customer-level RFM table to 'rfm_customer_segments.csv'")
print()

# ============================================================
# STEP 6: CHARTS
# ============================================================

plt.figure(figsize=(7, 4))
segment_counts = rfm["Segment"].value_counts()
plt.bar(segment_counts.index, segment_counts.values, color="#2563eb")
plt.title("Number of Customers per Segment")
plt.ylabel("Customers")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("chart_segment_counts.png", dpi=150)
plt.close()

plt.figure(figsize=(6, 5))
colors_map = {
    "Champions": "#16a34a", "Loyal Customers": "#22c55e",
    "At Risk": "#dc2626", "New / Recent": "#3b82f6",
    "Lost": "#6b7280", "Needs Attention": "#f59e0b",
}
for seg in rfm["Segment"].unique():
    sub = rfm[rfm["Segment"] == seg]
    plt.scatter(sub["Frequency"], sub["Monetary"], label=seg,
                color=colors_map.get(seg, "gray"), alpha=0.7)
plt.xlabel("Frequency (number of orders)")
plt.ylabel("Monetary (total spend $)")
plt.title("Customer Segments: Frequency vs Monetary Value")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("chart_frequency_vs_monetary.png", dpi=150)
plt.close()

print("=== STEP 6: Charts saved ===")
print("- chart_segment_counts.png")
print("- chart_frequency_vs_monetary.png")
print()

# ============================================================
# STEP 7: THE INSIGHT
# ============================================================
at_risk_row = segment_summary.loc["At Risk"] if "At Risk" in segment_summary.index else None
champions_row = segment_summary.loc["Champions"] if "Champions" in segment_summary.index else None

print("=== STEP 7: Key Insight ===")
if at_risk_row is not None:
    print(f"- 'At Risk' customers: {at_risk_row['num_customers']} people "
          f"({at_risk_row['pct_of_customers']}% of customers) but "
          f"{at_risk_row['pct_of_revenue']}% of historical revenue")
if champions_row is not None:
    print(f"- 'Champions': {champions_row['num_customers']} people "
          f"({champions_row['pct_of_customers']}% of customers) driving "
          f"{champions_row['pct_of_revenue']}% of revenue")
print()
print("Write this as one sentence for your resume, e.g.:")
print('  "At-Risk customers represented [X]% of customers but historically')
print('   contributed [Y]% of revenue - recommend a targeted win-back campaign')
print('   before that revenue is lost for good."')