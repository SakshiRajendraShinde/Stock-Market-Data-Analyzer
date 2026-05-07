import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Create folders
folders = ["data", "outputs", "reports", "images"]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# -------------------------------
# USER INPUT
# -------------------------------

ticker = input("Enter Stock Ticker Symbol (Example: AAPL): ")

start_date = input("Enter Start Date (YYYY-MM-DD): ")
end_date = input("Enter End Date (YYYY-MM-DD): ")

# -------------------------------
# FETCH STOCK DATA
# -------------------------------

print("\nFetching stock data...")

df = yf.download(ticker, start=start_date, end=end_date)

if df.empty:
    print("No data found.")
    exit()

# Save raw data
raw_file = f"data/{ticker}_stock_data.csv"
df.to_csv(raw_file)

print(f"Data saved to {raw_file}")

# -------------------------------
# DATA CLEANING
# -------------------------------

df.dropna(inplace=True)

# -------------------------------
# DAILY RETURNS
# -------------------------------

df['Daily Return'] = df['Close'].pct_change()

# -------------------------------
# MOVING AVERAGES
# -------------------------------

df['20 Day MA'] = df['Close'].rolling(window=20).mean()
df['50 Day MA'] = df['Close'].rolling(window=50).mean()

# -------------------------------
# VOLATILITY
# -------------------------------

volatility = df['Daily Return'].std()

# -------------------------------
# HIGH/LOW ANALYSIS
# -------------------------------

highest_price = df['High'].max()
lowest_price = df['Low'].min()

# -------------------------------
# SUMMARY REPORT
# -------------------------------

summary = f"""
STOCK MARKET ANALYSIS REPORT
============================

Ticker Symbol: {ticker}

Start Date: {start_date}
End Date: {end_date}

Highest Price: {highest_price:.2f}
Lowest Price: {lowest_price:.2f}

Average Daily Return:
{df['Daily Return'].mean():.4f}

Volatility:
{volatility:.4f}

Total Records:
{len(df)}
"""

print(summary)

# Save report
report_file = f"reports/{ticker}_report.txt"

with open(report_file, "w") as file:
    file.write(summary)

print(f"Report saved to {report_file}")

# -------------------------------
# VISUALIZATION
# -------------------------------

sns.set_style("darkgrid")

# Closing Price Chart
plt.figure(figsize=(12,6))
plt.plot(df['Close'], label='Closing Price')
plt.title(f'{ticker} Closing Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

close_chart = f"images/{ticker}_closing_price.png"
plt.savefig(close_chart)
plt.close()

# Moving Average Chart
plt.figure(figsize=(12,6))
plt.plot(df['Close'], label='Closing Price')
plt.plot(df['20 Day MA'], label='20 Day MA')
plt.plot(df['50 Day MA'], label='50 Day MA')

plt.title(f'{ticker} Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

ma_chart = f"images/{ticker}_moving_average.png"
plt.savefig(ma_chart)
plt.close()

# Daily Return Distribution
plt.figure(figsize=(10,5))

sns.histplot(df['Daily Return'].dropna(), bins=50)

plt.title(f'{ticker} Daily Return Distribution')

returns_chart = f"images/{ticker}_returns_distribution.png"
plt.savefig(returns_chart)
plt.close()

print("\nCharts saved successfully.")

# -------------------------------
# SAVE FINAL DATA
# -------------------------------

output_csv = f"outputs/{ticker}_processed_data.csv"

df.to_csv(output_csv)

print(f"Processed data saved to {output_csv}")

print("\nAnalysis Completed Successfully.")